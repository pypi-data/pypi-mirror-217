
import asyncio
import pickle
import socket
import ssl
import zstandard
from collections import deque, defaultdict
from mercury_sync.encryption import AESGCMFernet
from mercury_sync.env import Env
from mercury_sync.env.time_parser import TimeParser
from mercury_sync.models.message import Message
from mercury_sync.snowflake.snowflake_generator import SnowflakeGenerator
from typing import (
    Tuple, 
    Deque, 
    Any, 
    Dict, 
    Coroutine, 
    AsyncIterable,
    Union,
    Optional
)
from mercury_sync.connection.tcp.protocols import (
    MercurySyncTCPClientProtocol,
    MercurySyncTCPServerProtocol
)


class MercurySyncTCPConnection:

    def __init__(
        self,
        host: str,
        port: int,
        instance_id: int,
        env: Env
    ) -> None:

        self.id_generator = SnowflakeGenerator(instance_id)
        self.env = env

        self.host = host
        self.port = port

        self.events: Dict[
            str,
            Coroutine
        ] = {}

        self.queue: Dict[str, Deque[Tuple[str, int, float, Any]] ] = defaultdict(deque)
        self.parsers: Dict[str, Message] = {}
        self.connected = False
        self._running = False

        self._client_transports: Dict[str, asyncio.Transport] = {}
        self._server: asyncio.Server = None
        self._loop: Union[asyncio.AbstractEventLoop, None] = None
        self._waiters: Dict[str, Deque[asyncio.Future]] = defaultdict(deque)
        self._pending_responses: Deque[asyncio.Task]= deque()
        self._last_call: Deque[str] = deque()

        self._sent_values = deque()
        self._server_socket = None
        self._stream = False
        
        self._client_key_path: Union[str, None] = None
        self._client_cert_path: Union[str, None] = None

        self._server_key_path: Union[str, None] = None
        self._server_cert_path: Union[str, None] = None 
        
        self._client_ssl_context: Union[ssl.SSLContext, None] = None
        self._server_ssl_context: Union[ssl.SSLContext, None] = None
        
        self._encryptor = AESGCMFernet(env)
        self._semaphore: Union[asyncio.Semaphore, None] = None
        self._compressor: Union[zstandard.ZstdCompressor, None] = None
        self._decompressor: Union[zstandard.ZstdDecompressor, None] = None
        self._cleanup_task: Union[asyncio.Task, None] = None
        self._sleep_task: Union[asyncio.Task, None] = None
        self._cleanup_interval = TimeParser(env.MERCURY_SYNC_CLEANUP_INTERVAL).time
        self._max_concurrency = env.MERCURY_SYNC_MAX_CONCURRENCY
        self._tcp_connect_retries = env.MERCURY_SYNC_TCP_CONNECT_RETRIES

    def connect(
        self,
        cert_path: Optional[str]=None,
        key_path: Optional[str]=None,
        worker_socket: Optional[socket.socket]=None
    ):

        try:

            self._loop = asyncio.get_event_loop()

        except Exception:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
        self._running = True
        self._semaphore = asyncio.Semaphore(self._max_concurrency)

        self._compressor = zstandard.ZstdCompressor()
        self._decompressor = zstandard.ZstdDecompressor()

        if cert_path and key_path:
            self._server_ssl_context = self._create_server_ssl_context(
                cert_path=cert_path,
                key_path=key_path
            ) 

        if self.connected is False and worker_socket is None:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.bind((self.host, self.port))

            self._server_socket.setblocking(False)

        elif self.connected is False:
            self._server_socket = worker_socket
            host, port = worker_socket.getsockname()
            self.host = host
            self.port = port

        if self.connected is False:

            server = self._loop.create_server(
                lambda: MercurySyncTCPServerProtocol(
                    self.read
                ),
                sock=self._server_socket,
                ssl=self._server_ssl_context
            )

            self._server = self._loop.run_until_complete(server)

            self.connected = True

            self._cleanup_task = self._loop.create_task(self._cleanup())

    async def connect_async(
        self,
        cert_path: Optional[str]=None,
        key_path: Optional[str]=None,
        worker_socket: Optional[socket.socket]=None
    ):

        try:

            self._loop = asyncio.get_event_loop()

        except Exception:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

        self._running = True
        self._semaphore = asyncio.Semaphore(self._max_concurrency)

        self._compressor = zstandard.ZstdCompressor()
        self._decompressor = zstandard.ZstdDecompressor()

        if cert_path and key_path:
            self._server_ssl_context = self._create_server_ssl_context(
                cert_path=cert_path,
                key_path=key_path
            ) 

        if self.connected is False and worker_socket is None:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                self._server_socket.bind((self.host, self.port))

            except Exception:
                pass


            self._server_socket

            self._server_socket.setblocking(False)

        elif self.connected is False:
            self._server_socket = worker_socket
            host, port = worker_socket.getsockname()
            self.host = host
            self.port = port

        if self.connected is False:

            server = self._loop.create_server(
                lambda: MercurySyncTCPServerProtocol(
                    self.read
                ),
                sock=self._server_socket,
                ssl=self._server_ssl_context
            )

            self._server = await server
            self.connected = True

            self._cleanup_task = self._loop.create_task(self._cleanup())

    def _create_server_ssl_context(
        self, 
        cert_path: Optional[str]=None,
        key_path: Optional[str]=None
    ) -> ssl.SSLContext:
        
        if self._server_cert_path is None:
            self._server_cert_path = cert_path

        if self._server_key_path is None:
            self._server_key_path = key_path

        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_ctx.options |= ssl.OP_NO_TLSv1
        ssl_ctx.options |= ssl.OP_NO_TLSv1_1
        ssl_ctx.options |= ssl.OP_SINGLE_DH_USE
        ssl_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        ssl_ctx.load_cert_chain(cert_path, keyfile=key_path)
        ssl_ctx.load_verify_locations(cafile=cert_path)
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
        ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

        return ssl_ctx

    async def connect_client(
        self,
        address: Tuple[str, int],
        cert_path: Optional[str]=None,
        key_path: Optional[str]=None
    ) -> Coroutine[Any, Any, asyncio.Transport]:
        
        self._loop = asyncio.get_event_loop()
        if cert_path and key_path:
            self._client_ssl_context = self._create_client_ssl_context(
                cert_path=cert_path,
                key_path=key_path
            ) 

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        await self._loop.run_in_executor(None, tcp_socket.connect, address)

        tcp_socket.setblocking(False)

        last_error: Union[Exception, None] = None

        for _ in range(self._tcp_connect_retries):

            try:

                client_transport, _ = await self._loop.create_connection(
                    lambda: MercurySyncTCPClientProtocol(
                        self.read
                    ),
                    sock=tcp_socket,
                    ssl=self._client_ssl_context
                )

                self._client_transports[address] = client_transport

                return client_transport
            
            except ConnectionRefusedError as connection_error:
                last_error = connection_error

            await asyncio.sleep(1)

        if last_error:
            raise last_error
    
    def _create_client_ssl_context(
        self, 
        cert_path: Optional[str]=None,
        key_path: Optional[str]=None
    ) -> ssl.SSLContext:
        
        if self._client_cert_path is None:
            self._client_cert_path = cert_path

        if self._client_key_path is None:
            self._client_key_path = key_path

        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_ctx.options |= ssl.OP_NO_TLSv1
        ssl_ctx.options |= ssl.OP_NO_TLSv1_1
        ssl_ctx.load_cert_chain(cert_path, keyfile=key_path)
        ssl_ctx.load_verify_locations(cafile=cert_path)
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
        ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

        return ssl_ctx
    
    async def _cleanup(self):
        while self._running:
            self._sleep_task = asyncio.create_task(
                asyncio.sleep(self._cleanup_interval)
            )

            await self._sleep_task

            for pending in list(self._pending_responses):
                if pending.done() or pending.cancelled():

                    try:
                        await pending

                    except Exception:
                        await self.close()
                        await self.connect_async(
                            cert_path=self._client_cert_path,
                            key_path=self._client_key_path
                        )

                    self._pending_responses.pop()

    async def send(
        self, 
        event_name: bytes,
        data: bytes, 
        address: Tuple[str, int]
    ) -> Tuple[int, Dict[str, Any]]:
        
        async with self._semaphore:
            self._last_call.append(event_name)

            client_transport = self._client_transports.get(address)
            if client_transport is None:
                await self.connect_client(
                    address,
                    cert_path=self._client_cert_path,
                    key_path=self._client_key_path
                )

                client_transport = self._client_transports.get(address)

            item = pickle.dumps(
                (
                    'request',
                    self.id_generator.generate(),
                    event_name,
                    data,
                    self.host,
                    self.port
                ),
                protocol=pickle.HIGHEST_PROTOCOL
            )

            encrypted_message = self._encryptor.encrypt(item)
            compressed = self._compressor.compress(encrypted_message)

            client_transport.write(compressed)

            waiter = self._loop.create_future()
            self._waiters[event_name].append(waiter)

            await waiter

            (
                _,
                shard_id,
                _,
                response_data,
                _, 
                _
            ) = self.queue[event_name].pop()

            return (
                shard_id,
                response_data
            )
    
    async def stream(
        self, 
        event_name: str,
        data: Any, 
        address: Tuple[str, int]
    ) -> AsyncIterable[Tuple[int, Dict[str, Any]]]: 
        
        async with self._semaphore:
            self._last_call.append(event_name)

            client_transport = self._client_transports.get(address)


            if self._stream is False:
                item = pickle.dumps(
                    (
                        'stream_connect',
                        self.id_generator.generate(),
                        event_name,
                        data,
                        self.host,
                        self.port
                    ),
                    protocol=pickle.HIGHEST_PROTOCOL
                )


            else:
                item = pickle.dumps(
                    (
                        'stream',
                        self.id_generator.generate(),
                        event_name,
                        data,
                        self.host,
                        self.port
                    ),
                    protocol=pickle.HIGHEST_PROTOCOL
                )

            encrypted_message = self._encryptor.encrypt(item)
            compressed = self._compressor.compress(encrypted_message)

            client_transport.write(compressed)

            waiter = self._loop.create_future()
            self._waiters[event_name].append(waiter)

            await waiter

            if self._stream is False:

                self.queue[event_name].pop()

                self._stream = True

                item = pickle.dumps(
                    (
                        'stream',
                        self.id_generator.generate(),
                        event_name,
                        data,
                        self.host,
                        self.port
                    ),
                    pickle.HIGHEST_PROTOCOL
                )

                encrypted_message = self._encryptor.encrypt(item)
                compressed = self._compressor.compress(encrypted_message)

                client_transport.write(compressed)

                waiter = self._loop.create_future()
                self._waiters[event_name].append(waiter)

                await waiter


            while bool(self.queue[event_name]) and self._stream:

                (
                    _,
                    shard_id,
                    _,
                    response_data,
                    _, 
                    _
                ) = self.queue[event_name].pop()
            
                yield(
                    shard_id,
                    response_data
                )


        self.queue.clear()

    def read(
        self,
        data: bytes,
        transport: asyncio.Transport
    ) -> None:
        decompressed = b''

        try:
            decompressed = self._decompressor.decompress(data)

        except Exception as decompression_error:
            self._pending_responses.append(
                asyncio.create_task(
                    self._send_error(
                        error_message=str(decompression_error),
                        transport=transport
                    )
                )
            )

            if bool(self._last_call):
                event_name = self._last_call.pop()
                event_waiter = self._waiters[event_name]

                if bool(event_waiter):
                    waiter = event_waiter.pop()

                    try:

                        waiter.set_result(None)

                    except asyncio.InvalidStateError:
                        pass

            return

        decrypted = self._encryptor.decrypt(decompressed)

        result: Tuple[
            str, 
            int, 
            float, 
            Any, 
            str, 
            int
        ] = pickle.loads(decrypted)

        (
            message_type, 
            shard_id, 
            event_name,
            payload, 
            incoming_host, 
            incoming_port
        ) = result

        if message_type == 'request':
            self._pending_responses.append(
                asyncio.create_task(
                    self._read(
                        event_name,
                        self.events.get(event_name)(
                            shard_id,
                            self.parsers[event_name](**payload)
                        ),
                        transport
                    )
                )
            )

        elif message_type == "stream_connect":

            self.queue[event_name].append((
                message_type, 
                shard_id,
                event_name,
                payload, 
                incoming_host,
                incoming_port
            ))

            self._pending_responses.append(
                asyncio.create_task(
                    self._initialize_stream(
                        event_name,
                        transport
                    )
                )
            )

            event_waiter = self._waiters[event_name]

            if bool(event_waiter):
                waiter = event_waiter.pop()

                try:

                    waiter.set_result(None)

                except asyncio.InvalidStateError:
                    pass

        elif message_type == 'stream' or message_type == "stream_connect":

            self.queue[event_name].append((
                message_type, 
                shard_id,
                event_name,
                payload, 
                incoming_host,
                incoming_port
            ))

            self._pending_responses.append(
                asyncio.create_task(
                    self._read_iterator(
                        event_name,
                        self.events.get(event_name)(
                            shard_id,
                            self.parsers[event_name](**payload)
                        ),
                        transport
                    )
                )
            )

            event_waiter = self._waiters[event_name]

            if bool(event_waiter):
                waiter = event_waiter.pop()

                try:

                    waiter.set_result(None)

                except asyncio.InvalidStateError:
                    pass

        else:

            if event_name is None and bool(self._last_call):
                event_name = self._last_call.pop()

            self.queue[event_name].append((
                message_type, 
                shard_id,
                event_name,
                payload, 
                incoming_host,
                incoming_port
            ))

                
            event_waiter = self._waiters[event_name]

            if bool(event_waiter):
                waiter = event_waiter.pop()

                try:

                    waiter.set_result(None)

                except asyncio.InvalidStateError:
                    pass

    async def _read(
        self,
        event_name: str,
        coroutine: Coroutine,
        transport: asyncio.Transport
    ) -> Coroutine[Any, Any, None]:
        response: Message = await coroutine

        item = pickle.dumps(
            (
                'response', 
                self.id_generator.generate(),
                event_name,
                response.to_data(), 
                self.host,
                self.port
            ),
            protocol=pickle.HIGHEST_PROTOCOL
        )

        encrypted_message = self._encryptor.encrypt(item)
        compressed = self._compressor.compress(encrypted_message)

        transport.write(compressed)

    async def _read_iterator(
        self,
        event_name: str,
        coroutine: AsyncIterable[Message],
        transport: asyncio.Transport       
    ) -> Coroutine[Any, Any, None]:
  
        async for response in coroutine:
            item = pickle.dumps(
                (
                    'response', 
                    self.id_generator.generate(),
                    event_name,
                    response.to_data(), 
                    self.host,
                    self.port
                ),
                protocol=pickle.HIGHEST_PROTOCOL
            )

            encrypted_message = self._encryptor.encrypt(item)
            compressed = self._compressor.compress(encrypted_message)

            transport.write(compressed)

    async def _initialize_stream(
        self,
        event_name: str,
        transport: asyncio.Transport            
    ) -> Coroutine[Any, Any, None]:
        message = Message()
        item = pickle.dumps(
            (
                'response', 
                self.id_generator.generate(),
                event_name,
                message.to_data(), 
                self.host,
                self.port
            ),
            protocol=pickle.HIGHEST_PROTOCOL
        )

        encrypted_message = self._encryptor.encrypt(item)
        compressed = self._compressor.compress(encrypted_message)

        transport.write(compressed)

    async def _send_error(
        self,
        error_message: str,
        transport: asyncio.Transport
    ) -> Coroutine[Any, Any, None]:
        
        error = Message(
            error=error_message
        )

        item = pickle.dumps(
            (
                'response', 
                self.id_generator.generate(),
                None,
                error.to_data(), 
                self.host,
                self.port
            ),
            protocol=pickle.HIGHEST_PROTOCOL
        )

        encrypted_message = self._encryptor.encrypt(item)
        compressed = self._compressor.compress(encrypted_message)

        transport.write(compressed)
        
    async def close(self) -> None:
        self._stream = False
        self._running = False

        for client in self._client_transports.values():
            client.abort()
        
        if self._cleanup_task:
            self._cleanup_task.cancel()
            if self._cleanup_task.cancelled() is False:
                try:
                    self._sleep_task.cancel()
                    if not self._sleep_task.cancelled():
                        await self._sleep_task

                except asyncio.CancelledError:
                    pass

                try:

                    await self._cleanup_task

                except asyncio.CancelledError:
                    pass

            