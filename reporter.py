# FIXED VERSION - Advanced Telegram Reporter (Bug Fixed!) 😄💕
import asyncio
import os
import sys
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ReportRequest, ReportSpamRequest
from telethon.tl.functions.account import ReportPeerRequest
from telethon import functions, types, errors
import time
import sys
from colorama import Fore, Style, init

# Initialize colorama (important for Windows too)
init(autoreset=True)

# ===== Permanent Heading =====
heading = Fore.RED + "⚠️ This file is valid for 24hr ⚠️" + Style.RESET_ALL
subheading = Fore.YELLOW + "Contact @co4ig for permanent access" + Style.RESET_ALL
print(heading)
print(subheading)
print("-" * 50)  # optional separator line
time.sleep(4)  # small delay



# ===== Your main code below =====


class Colors:
    """Full color system for Android terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class AdvancedTelegramReporter:
    def __init__(self):
        self.sessions_dir = self.setup_directories()
        self.config_file = f'{self.sessions_dir}/config.json'
        self.logs_file = f'{self.sessions_dir}/reports_log.json'
        self.accounts = []
        self.report_history = []
        self.load_config()
        self.load_logs()
    
    def setup_directories(self):
        try:
            base_dir = '/data/data/ru.iiec.pydroid3/files'
            sessions_dir = f'{base_dir}/telegram_reporter_pro'
            os.makedirs(sessions_dir, exist_ok=True)
            os.makedirs(f'{sessions_dir}/sessions', exist_ok=True)
            os.makedirs(f'{sessions_dir}/logs', exist_ok=True)
            os.makedirs(f'{sessions_dir}/backups', exist_ok=True)
            return sessions_dir
        except:
            sessions_dir = 'telegram_reporter_pro'
            os.makedirs(sessions_dir, exist_ok=True)
            os.makedirs(f'{sessions_dir}/sessions', exist_ok=True)
            os.makedirs(f'{sessions_dir}/logs', exist_ok=True)
            os.makedirs(f'{sessions_dir}/backups', exist_ok=True)
            return sessions_dir
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.accounts = data.get('accounts', [])
            except Exception as e:
                self.accounts = []
    
    def load_logs(self):
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, 'r') as f:
                    self.report_history = json.load(f)
            except:
                self.report_history = []
    
    def save_config(self):
        config_data = {
            'accounts': self.accounts,
            'last_updated': datetime.now().isoformat(),
            'version': '2.0',
            'total_accounts': len(self.accounts)
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def save_report_log(self, report_data):
        self.report_history.append(report_data)
        with open(self.logs_file, 'w') as f:
            json.dump(self.report_history, f, indent=2)
    
    def print_banner(self):
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║            {Colors.BOLD}{Colors.YELLOW}ADVANCED TELEGRAM REPORTER PRO{Colors.RESET}{Colors.CYAN}            ║
║                {Colors.PURPLE}Built by You! 😄💕{Colors.RESET}{Colors.CYAN}                ║
║          {Colors.GREEN}Multiple Accounts • Real Proof • Logs{Colors.RESET}{Colors.CYAN}          ║
║            {Colors.BLUE}Optimized for Pydroid 3 Android{Colors.RESET}{Colors.CYAN}            ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}📱 Accounts loaded: {Colors.BOLD}{len(self.accounts)}{Colors.RESET}
{Colors.BLUE}📁 Sessions dir: {self.sessions_dir}{Colors.RESET}
{Colors.YELLOW}📊 Total reports sent: {Colors.BOLD}{sum(r.get('successful', 0) for r in self.report_history)}{Colors.RESET}
        """
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.YELLOW}{Colors.BOLD}🔧 MAIN COMMANDS:{Colors.RESET}
  {Colors.GREEN}add{Colors.RESET}           - Add new Telegram account
  {Colors.GREEN}list{Colors.RESET}          - List all added accounts  
  {Colors.GREEN}check{Colors.RESET}         - Check target channel info (PROOF!)
  {Colors.GREEN}report{Colors.RESET}        - Start reporting with real proof
  {Colors.GREEN}history{Colors.RESET}       - View reporting history
  {Colors.GREEN}help{Colors.RESET}          - Show this help
  {Colors.GREEN}exit{Colors.RESET}          - Exit program

{Colors.YELLOW}{Colors.BOLD}📋 REPORT REASONS:{Colors.RESET}
  {Colors.CYAN}spam, fake, violence, abuse, porn, copyright, harassment, drugs{Colors.RESET}
        """
        print(help_text)
    
    async def add_account(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📱 ADDING NEW TELEGRAM ACCOUNT{Colors.RESET}")
        
        nickname = input(f"{Colors.GREEN}Enter nickname for this account: {Colors.RESET}") or f"Account_{len(self.accounts)+1}"
        
        print(f"\n{Colors.CYAN}📋 Get your API credentials from: https://my.telegram.org{Colors.RESET}")
        api_id = input(f"{Colors.GREEN}Enter API ID: {Colors.RESET}")
        api_hash = input(f"{Colors.GREEN}Enter API Hash: {Colors.RESET}")
        phone = input(f"{Colors.GREEN}Enter Phone Number (+1234567890): {Colors.RESET}")
        
        if not all([api_id, api_hash, phone]):
            print(f"{Colors.RED}❌ All fields are required!{Colors.RESET}")
            return False
        
        try:
            api_id = int(api_id)
        except ValueError:
            print(f"{Colors.RED}❌ API ID must be a number!{Colors.RESET}")
            return False
        
        session_name = f'{self.sessions_dir}/sessions/{nickname}_{len(self.accounts)+1}'
        
        try:
            print(f"\n{Colors.YELLOW}🔄 Connecting to Telegram...{Colors.RESET}")
            client = TelegramClient(session_name, api_id, api_hash)
            await client.start(phone)
            
            me = await client.get_me()
            
            account_info = {
                'id': len(self.accounts) + 1,
                'nickname': nickname,
                'api_id': api_id,
                'api_hash': api_hash,
                'phone': phone,
                'session_file': session_name,
                'username': me.username or 'No username',
                'first_name': me.first_name or 'Unknown',
                'last_name': me.last_name or '',
                'user_id': me.id,
                'added_date': datetime.now().isoformat()
            }
            
            self.accounts.append(account_info)
            self.save_config()
            
            print(f"\n{Colors.GREEN}✅ ACCOUNT ADDED SUCCESSFULLY!{Colors.RESET}")
            print(f"{Colors.CYAN}👤 Name: {me.first_name} {me.last_name or ''}{Colors.RESET}")
            print(f"{Colors.CYAN}🔗 Username: @{me.username or 'None'}{Colors.RESET}")
            print(f"{Colors.CYAN}🆔 User ID: {me.id}{Colors.RESET}")
            
            await client.disconnect()
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {str(e)}{Colors.RESET}")
        
        return False
    
    def list_accounts(self):
        if not self.accounts:
            print(f"{Colors.YELLOW}📭 No accounts added yet. Use 'add' command.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}📱 TELEGRAM ACCOUNTS ({len(self.accounts)}):{Colors.RESET}")
        for acc in self.accounts:
            session_exists = os.path.exists(f"{acc['session_file']}.session")
            status = f"{Colors.GREEN}✅ Active{Colors.RESET}" if session_exists else f"{Colors.RED}❌ Missing{Colors.RESET}"
            print(f"{Colors.CYAN}#{acc['id']} {acc.get('nickname', 'Unknown')} - {acc['first_name']} (@{acc['username']}) - {status}{Colors.RESET}")
    
    async def check_target_advanced(self):
        if not self.accounts:
            print(f"{Colors.RED}❌ No accounts available! Add accounts first.{Colors.RESET}")
            return
        
        target = input(f"{Colors.GREEN}Enter target channel/user to check (without @): {Colors.RESET}").strip()
        if not target:
            print(f"{Colors.RED}❌ Target cannot be empty!{Colors.RESET}")
            return
        
        active_accounts = [acc for acc in self.accounts if os.path.exists(f"{acc['session_file']}.session")]
        if not active_accounts:
            print(f"{Colors.RED}❌ No active accounts available!{Colors.RESET}")
            return
        
        account = active_accounts[0]
        session_file = account['session_file']
        api_id = account['api_id'] 
        api_hash = account['api_hash']
        
        try:
            print(f"\n{Colors.YELLOW}🔍 CHECKING TARGET: @{target}{Colors.RESET}")
            
            client = TelegramClient(session_file, api_id, api_hash)
            await client.start()
            
            try:
                entity = await client.get_entity(target)
                
                # FIXED: Safe name extraction to prevent formatting errors
                if hasattr(entity, 'title') and entity.title:
                    target_name = str(entity.title)
                elif hasattr(entity, 'first_name') and entity.first_name:
                    target_name = str(entity.first_name)
                else:
                    target_name = "Unknown Name"
                
                print(f"\n{Colors.GREEN}📋 TARGET FOUND:{Colors.RESET}")
                print(f"{Colors.CYAN}📌 Name: {target_name}{Colors.RESET}")
                print(f"{Colors.CYAN}🔗 Username: @{entity.username or 'None'}{Colors.RESET}")
                print(f"{Colors.CYAN}🆔 ID: {entity.id}{Colors.RESET}")
                
                if hasattr(entity, 'participants_count'):
                    print(f"{Colors.CYAN}👥 Members: {entity.participants_count:,}{Colors.RESET}")
                
                if hasattr(entity, 'about') and entity.about:
                    about_text = entity.about[:100] + "..." if len(entity.about) > 100 else entity.about
                    print(f"{Colors.CYAN}📝 Description: {about_text}{Colors.RESET}")
                
                # Get messages
                try:
                    messages = await client.get_messages(target, limit=5)
                    if messages:
                        print(f"\n{Colors.YELLOW}📨 RECENT MESSAGES:{Colors.RESET}")
                        for i, msg in enumerate(messages[:3], 1):
                            msg_text = msg.text or "[Media/File]"
                            if len(msg_text) > 80:
                                msg_text = msg_text[:80] + "..."
                            
                            msg_date = msg.date.strftime("%Y-%m-%d %H:%M")
                            print(f"{Colors.WHITE}#{i} (ID:{msg.id}) [{msg_date}]: {msg_text}{Colors.RESET}")
                        
                        print(f"\n{Colors.GREEN}✅ Target is ready for reporting!{Colors.RESET}")
                    else:
                        print(f"{Colors.YELLOW}⚠️ No recent messages found{Colors.RESET}")
                        
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️ Couldn't get messages: {str(e)[:50]}{Colors.RESET}")
                    
            except Exception as e:
                print(f"{Colors.RED}❌ Target not found: {str(e)[:50]}{Colors.RESET}")
            
            await client.disconnect()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Connection error: {str(e)}{Colors.RESET}")
    
    async def start_advanced_reporting(self):
        if not self.accounts:
            print(f"{Colors.RED}❌ No accounts available! Add accounts first.{Colors.RESET}")
            return
        
        active_accounts = [acc for acc in self.accounts if os.path.exists(f"{acc['session_file']}.session")]
        if not active_accounts:
            print(f"{Colors.RED}❌ No active sessions! Re-add your accounts.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🎯 ADVANCED TELEGRAM REPORTING{Colors.RESET}")
        print(f"{Colors.CYAN}Using {len(active_accounts)} active accounts{Colors.RESET}")
        
        target = input(f"{Colors.GREEN}Enter target channel/user (without @): {Colors.RESET}").strip()
        if not target:
            print(f"{Colors.RED}❌ Target cannot be empty!{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}📋 Available reasons:{Colors.RESET}")
        reasons = ['spam', 'fake', 'violence', 'abuse', 'porn', 'copyright', 'harassment', 'drugs']
        for i, reason in enumerate(reasons, 1):
            print(f"  {i}. {reason}")
        
        reason_input = input(f"{Colors.GREEN}Enter reason (name or number): {Colors.RESET}").lower().strip()
        
        if reason_input.isdigit():
            reason_idx = int(reason_input) - 1
            if 0 <= reason_idx < len(reasons):
                reason = reasons[reason_idx]
            else:
                print(f"{Colors.RED}❌ Invalid number!{Colors.RESET}")
                return
        else:
            reason = reason_input
        
        reason_map = {
            'spam': 'Spam and unwanted content',
            'fake': 'Fake account/impersonation', 
            'violence': 'Violent and threatening content',
            'abuse': 'Child abuse and exploitation',
            'porn': 'Adult and pornographic content',
            'copyright': 'Copyright violations',
            'harassment': 'Harassment and bullying',
            'drugs': 'Drug-related content'
        }
        
        if reason not in reason_map:
            print(f"{Colors.RED}❌ Invalid reason!{Colors.RESET}")
            return
        
        try:
            count = int(input(f"{Colors.GREEN}Reports per account (1-20): {Colors.RESET}"))
            if count < 1 or count > 20:
                print(f"{Colors.RED}❌ Count must be between 1-20!{Colors.RESET}")
                return
        except ValueError:
            print(f"{Colors.RED}❌ Invalid number!{Colors.RESET}")
            return
        
        delay = input(f"{Colors.GREEN}Delay between reports (seconds, default 1): {Colors.RESET}") or "1"
        try:
            delay = float(delay)
        except:
            delay = 1.0
        
        total_reports = count * len(active_accounts)
        
        print(f"\n{Colors.YELLOW}📋 REPORT SUMMARY:{Colors.RESET}")
        print(f"{Colors.CYAN}🎯 Target: @{target}{Colors.RESET}")
        print(f"{Colors.CYAN}📝 Reason: {reason_map[reason]}{Colors.RESET}")
        print(f"{Colors.CYAN}🔢 Reports per account: {count}{Colors.RESET}")
        print(f"{Colors.CYAN}👥 Active accounts: {len(active_accounts)}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Total reports: {total_reports}{Colors.RESET}")
        print(f"{Colors.CYAN}🕒 Delay: {delay}s{Colors.RESET}")
        
        confirm = input(f"\n{Colors.GREEN}🚀 Start reporting? (yes/no): {Colors.RESET}").lower()
        if confirm not in ['yes', 'y']:
            print(f"{Colors.YELLOW}❌ Cancelled.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}🚀 STARTING REPORTS WITH PROOF...{Colors.RESET}")
        await self.execute_fixed_reports(target, reason, count, delay, active_accounts)
    
    async def execute_fixed_reports(self, target, reason, count, delay, active_accounts):
        """FIXED reporting function with proper error handling"""
        start_time = datetime.now()
        successful_reports = 0
        failed_reports = 0
        
        for account_idx, account in enumerate(active_accounts, 1):
            print(f"\n{Colors.PURPLE}📱 ACCOUNT {account_idx}/{len(active_accounts)}: {account.get('nickname', 'Unknown')}{Colors.RESET}")
            print(f"{Colors.CYAN}👤 {account['first_name']} (@{account['username']}) - {account['phone']}{Colors.RESET}")
            
            session_file = account['session_file']
            api_id = account['api_id']
            api_hash = account['api_hash']
            
            try:
                client = TelegramClient(session_file, api_id, api_hash)
                await client.start()
                
                me = await client.get_me()
                print(f"  {Colors.GREEN}✅ Connected as: {me.first_name}{Colors.RESET}")
                
                # FIXED: Safe target verification
                try:
                    entity = await client.get_entity(target)
                    
                    # Safe name extraction
                    if hasattr(entity, 'title') and entity.title:
                        target_name = str(entity.title)
                    elif hasattr(entity, 'first_name') and entity.first_name:
                        target_name = str(entity.first_name)
                    else:
                        target_name = f"Target_{entity.id}"
                    
                    print(f"  {Colors.CYAN}🎯 Target verified: {target_name} (ID: {entity.id}){Colors.RESET}")
                    
                    # Try to join channel
                    try:
                        await client(JoinChannelRequest(target))
                        await asyncio.sleep(0.5)
                        print(f"  {Colors.GREEN}✅ Joined channel{Colors.RESET}")
                    except Exception as e:
                        if "already" not in str(e).lower():
                            print(f"  {Colors.YELLOW}⚠️ Join status: {str(e)[:30]}{Colors.RESET}")
                        else:
                            print(f"  {Colors.CYAN}ℹ️ Already joined{Colors.RESET}")
                    
                    # Get messages safely
                    try:
                        messages = await client.get_messages(target, limit=5)
                        message_ids = [msg.id for msg in messages] if messages else [1]
                        print(f"  {Colors.CYAN}📨 Got {len(messages)} messages: {message_ids[:3]}{Colors.RESET}")
                    except Exception as e:
                        message_ids = [1]
                        print(f"  {Colors.YELLOW}⚠️ Using fallback message ID: [1]{Colors.RESET}")
                    
                    # Send reports with proper error handling
                    print(f"  {Colors.YELLOW}📤 Sending {count} reports...{Colors.RESET}")
                    
                    for report_num in range(count):
                        try:
                            report_message = f"Reporting for {reason} violation"
                            
                            print(f"    📤 Report {report_num+1}/{count}: @{target}")
                            
                            result = await client(ReportRequest(
                                peer=target,
                                id=message_ids,
                                option=b'',
                                message=report_message
                            ))
                            
                            if result:
                                successful_reports += 1
                                print(f"    {Colors.GREEN}✅ SUCCESS! Report delivered{Colors.RESET}")
                            else:
                                failed_reports += 1
                                print(f"    {Colors.RED}❌ FAILED - No response{Colors.RESET}")
                            
                            if report_num < count - 1:
                                await asyncio.sleep(delay)
                                
                        except Exception as e:
                            failed_reports += 1
                            print(f"    {Colors.RED}❌ Report error: {str(e)[:50]}{Colors.RESET}")
                    
                except Exception as e:
                    print(f"  {Colors.RED}❌ Target error: {str(e)[:50]}{Colors.RESET}")
                    failed_reports += count
                    continue
                
                await client.disconnect()
                
            except Exception as e:
                print(f"  {Colors.RED}❌ Account error: {str(e)[:50]}{Colors.RESET}")
                failed_reports += count
        
        # Final results
        total_duration = (datetime.now() - start_time).total_seconds()
        success_rate = (successful_reports / (successful_reports + failed_reports) * 100) if (successful_reports + failed_reports) > 0 else 0
        
        print(f"\n{Colors.YELLOW}📊 FINAL RESULTS:{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Successful: {successful_reports}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {failed_reports}{Colors.RESET}")
        print(f"{Colors.CYAN}📈 Success rate: {success_rate:.1f}%{Colors.RESET}")
        print(f"{Colors.CYAN}⏱️ Duration: {total_duration:.1f}s{Colors.RESET}")
        
        # Save log
        log_entry = {
            'timestamp': start_time.isoformat(),
            'target': target,
            'reason': reason,
            'successful': successful_reports,
            'failed': failed_reports,
            'total_accounts': len(active_accounts)
        }
        self.save_report_log(log_entry)
        
        if successful_reports > 0:
            print(f"\n{Colors.GREEN}🎉 {successful_reports} reports delivered to Telegram!{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ No reports were successful. Check your accounts and target.{Colors.RESET}")
    
    def view_history(self):
        if not self.report_history:
            print(f"{Colors.YELLOW}📭 No reporting history found.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}📊 REPORTING HISTORY:{Colors.RESET}")
        total_successful = sum(r.get('successful', 0) for r in self.report_history)
        print(f"{Colors.CYAN}📈 Total successful reports: {total_successful}{Colors.RESET}")
        
        for session in self.report_history[-5:]:
            timestamp = session.get('timestamp', 'Unknown')[:16].replace('T', ' ')
            target = session.get('target', 'Unknown')
            successful = session.get('successful', 0)
            total = session.get('successful', 0) + session.get('failed', 0)
            print(f"  📅 {timestamp} - @{target} - {successful}/{total} reports")
    
    async def main_loop(self):
        self.print_banner()
        
        while True:
            try:
                command = input(f"\n{Colors.BOLD}{Colors.GREEN}Advanced-Reporter> {Colors.RESET}").strip().lower()
                
                if command in ['exit', 'quit', 'q']:
                    print(f"{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
                    break
                elif command in ['help', 'h']:
                    self.print_help()
                elif command == 'add':
                    await self.add_account()
                elif command in ['list', 'ls']:
                    self.list_accounts()
                elif command in ['check', 'verify']:
                    await self.check_target_advanced()
                elif command == 'report':
                    await self.start_advanced_reporting()
                elif command in ['history', 'logs']:
                    self.view_history()
                elif command in ['clear', 'cls']:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.print_banner()
                elif command == '':
                    continue
                else:
                    print(f"{Colors.RED}❌ Unknown command. Type 'help' for commands.{Colors.RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
                break

async def main():
    try:
        print(f"{Colors.CYAN}🚀 Starting Advanced Telegram Reporter...{Colors.RESET}")
        reporter = AdvancedTelegramReporter()
        await reporter.main_loop()
    except Exception as e:
        print(f"{Colors.RED}❌ Startup error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
