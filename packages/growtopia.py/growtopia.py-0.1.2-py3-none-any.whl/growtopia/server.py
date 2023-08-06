__all__ = ("Server",)

import asyncio
from typing import Optional, Union

import enet

from .context import Context
from .dialog import Dialog
from .dispatcher import Dispatcher
from .enums import EventID
from .host import Host
from .player import Player, PlayerLoginInfo
from .protocol import GameMessagePacket, Packet, PacketType, TextPacket

# TODO:
# - Find a better way to ID peers. We used to ID peers by their connectID, but for some reason the attribute resets to 0 when the EVENT_TYPE_DISCONNECT event is emitted.


class Server(Host, Dispatcher):
    """
    Represents a Growtopia game server. This class uses the Host class as a base class and extends its functionality.
    This class is also used as a base class for other types of servers, such as ProxyServer and LoginServer.

    Parameters
    ----------
    address: tuple[str, int]
        The address to bind the server to.

    Kwarg Parameters
    ----------------
    peer_count: int
        The maximum amount of peers that can connect to the server.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.

    Attributes
    ----------
    players: dict[int, Player]
        A dictionary that has the peer id as the key and the Player object as the value.
    players_by_name: dict[str, Player]
        A dictionary that has the tank id name (player's username) as the key and the Player object as the value.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        Host.__init__(
            self,
            enet.Address(*address),
            kwargs.get("peer_count", 32),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )
        Dispatcher.__init__(self)

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.players: dict[str, Player] = {}  # players by address (host:port) instead of peer connectID (temporary)
        self.players_by_name: dict[str, Player] = {}

        self.running: bool = False

    def new_player(self, peer: enet.Peer) -> Player:
        """
        Instantiates a new Player object and adds it to the players dictionary.

        Parameters
        ----------
        peer: enet.Peer
            The peer to create a Player object for.

        Returns
        -------
        Player
            The Player object that was created.
        """
        player = Player(peer)
        self.players[str(peer.address)] = player

        return player

    def get_player(self, p: Union[enet.Peer, int, str]) -> Optional[Player]:
        """
        Retrieves a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to retrieve.

        Returns
        -------
        Optional[Player]
            The Player object that was retrieved, or None if nothing was found.
        """
        if isinstance(p, enet.Peer):
            return self.players.get(str(p.address), None)

        # if isinstance(p, int):
        #    return self.players.get(p, None)

        if isinstance(p, str):
            return self.players_by_name.get(p, None)

        return None

    def remove_player(self, p: Union[enet.Peer, int, str], disconnect: Optional[bool] = False) -> None:
        """
        Removes a player from the players dictionary.

        Parameters
        ----------
        p: Union[enet.Peer, int, str]
            The peer, peer id, or tank id name of the player to remove.
        """
        if player := self.get_player(p):
            self.players.pop(str(player.peer.address), None)
            self.players_by_name.pop(player.login_info.tankIDName, None)

            if disconnect:
                player.disconnect()

    def get_dialog(self, name: str) -> Optional[Dialog]:
        """
        Retreives a dialog from the dialogs dictionary.

        Parameters
        ----------
        name: str
            The name of the dialog to retrieve.

        Returns
        -------
        Optional[Dialog]
            The Dialog object that was retrieved, or None if nothing was found.
        """
        return self.dialogs.get(name, None)

    def start(self) -> None:
        """
        Starts the server.

        Returns
        -------
        None
        """
        self.running = True
        asyncio.run(self.run())

    def stop(self) -> None:
        """
        Stops the server.

        Returns
        -------
        None
        """
        self.running = False

    async def run(self) -> None:
        """
        Starts the asynchronous loop that handles events accordingly.

        Returns
        -------
        None
        """
        self.running = True
        await self.dispatch_event(EventID.ON_READY, self)

        while self.running:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            context = Context()
            context.server = self
            context.enet_event = event

            if event.type == enet.EVENT_TYPE_CONNECT:
                context.player = self.new_player(event.peer)
                await self.dispatch_event(EventID.ON_CONNECT, context)

                continue

            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                context.player = self.get_player(event.peer)

                await self.dispatch_event(EventID.ON_DISCONNECT, context)
                self.remove_player(event.peer)

                continue

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                context.player = self.get_player(event.peer)

                if (type_ := Packet.get_type(event.packet.data)) == PacketType.TEXT:
                    context.packet = TextPacket(event.packet.data)
                elif type_ == PacketType.GAME_MESSAGE:
                    context.packet = GameMessagePacket(event.packet.data)

                context.packet.sender = context.player
                event = context.packet.identify() if context.packet else EventID.ON_RECEIVE

                if event == EventID.ON_LOGIN_REQUEST:
                    context.player.login_info = PlayerLoginInfo(**context.packet.kvps)
                elif event == EventID.ON_DIALOG_RETURN:
                    dialog_name, button_clicked = context.packet.kvps.get("dialog_name", None), context.packet.kvps.get(
                        "buttonClicked", None
                    )

                    if dialog_name:
                        if await self.dispatch_dialog_return(dialog_name, button_clicked, context):
                            context.player.last_packet_received = context.packet
                            continue

                if not await self.dispatch_event(event, context):
                    await self.dispatch_event(
                        EventID.ON_UNHANDLED, context
                    )  # dispatch the ON_UNHANDLED event if the packet isn't handled by the user but recognised by growtopia.py

                context.player.last_packet_received = context.packet

        await self.dispatch_event(
            EventID.ON_CLEANUP,
            context,
        )
