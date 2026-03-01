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

import random
import requests

# Your proxy list (replace with your actual proxies)
proxies_list = [
    'socks5://72.49.49.11:31034',
'socks5://69.61.200.104:36181',
'socks5://66.42.224.229:41679',
'socks5://24.249.199.12:4145',
'socks5://192.111.137.37:18762',
'socks5://192.111.137.34:18765',
'socks5://192.111.139.163:19404',
'socks5://174.77.111.198:49547',
'socks5://184.178.172.28:15294',
'socks5://184.178.172.25:15291',
'socks5://184.178.172.18:15280',
'socks5://184.178.172.5:15303',
'socks5://184.178.172.23:4145',
'socks5://142.54.231.38:4145',
'socks5://67.201.59.70:4145',
'socks5://143.110.217.153:1080',
'socks5://64.227.131.240:1080',
'socks5://134.199.159.23:1080',
'socks5://198.177.252.24:4145',
'socks5://198.177.254.131:4145',
'socks5://192.241.156.17:1080',
'socks5://104.248.197.67:1080',
'socks5://104.248.203.234:1080',
'socks5://98.182.147.97:4145',
'socks5://72.223.188.67:4145',
'socks5://103.189.63.149:53053',
'socks5://121.169.46.116:1090',
'socks5://165.22.110.253:1080',
'socks5://124.248.168.90:1080',
'socks5://124.248.189.223:1080',
'socks5://194.163.182.6:1080',
'socks5://5.255.117.127:1080',
'socks5://5.255.113.177:1080',
'socks5://5.255.117.250:1080',
'socks5://104.219.236.127:1080',
'socks5://141.11.42.163:1080',
'socks5://221.224.56.210:10013',
'socks5://165.154.162.230:1080',
'socks5://103.148.112.69:8199',
'socks5://46.105.189.70:1090',
'socks5://217.171.94.214:10801',
'socks5://78.85.154.228:1080',
'socks5://113.20.28.68:1080',
'socks5://103.150.206.77:1080',
'socks5://95.165.82.189:1080',
'socks5://88.210.11.250:1080',
'socks5://115.127.53.114:1080',
'socks5://159.223.53.194:1080',
'socks5://149.62.186.244:1080',
'socks5://5.255.99.75:1080',
'socks5://13.70.6.6:50161',
'socks5://47.83.199.137:58367',
'socks5://43.99.243.123:58367',
'socks5://185.65.202.186:1080',
'socks5://114.35.9.239:1080',
'socks5://43.157.34.94:1777',
'socks5://43.131.9.114:1777',
'socks5://213.111.146.81:8888',
'socks5://173.249.5.133:1080',
'socks5://173.249.3.59:1080',
'socks5://194.233.68.54:1088',
'socks5://159.65.230.91:20067',
'socks5://43.160.195.20:20005',
'socks5://213.165.58.8:1080',
'socks5://185.208.74.38:1080',
'socks5://69.164.245.247:1080',
'socks5://109.172.84.215:1080',
'socks5://193.233.254.82:1080',
'socks5://213.165.58.7:1080',
'socks5://159.65.230.91:20547',
'socks5://37.59.249.78:1080',
'socks5://212.115.103.20:40000',
'socks5://148.251.88.242:1080',
'socks5://103.75.118.84:1080',
'socks5://212.34.135.86:5000',
'socks5://148.135.85.87:1080',
'socks5://156.244.39.41:20002',
'socks5://156.244.46.156:20002',
'socks5://156.244.2.246:20002',
'socks5://156.244.33.210:20002',
'socks5://156.244.39.37:20002',
'socks5://117.1.48.242:20036',
'socks5://83.228.227.81:1090',
'socks5://171.233.81.3:5000',
'socks5://171.233.80.188:5000',
'socks5://100.21.101.62:6000',
'socks5://206.123.156.251:5000',
'socks5://8.217.110.202:9999',
'socks5://206.123.156.228:4362',
'socks5://206.123.156.251:34304',
'socks4://208.102.51.6:58208',
'socks4://72.195.34.58:4145',
'socks4://184.181.217.210:4145',
'socks4://184.178.172.14:4145',
'socks4://184.181.217.206:4145',
'socks4://184.178.172.3:4145',
'socks4://184.178.172.11:4145',
'socks4://184.178.172.17:4145',
'socks4://184.181.217.213:4145',
'socks4://184.181.217.201:4145',
'socks4://184.181.217.194:4145',
'socks4://184.181.217.220:4145',
'socks4://192.111.138.29:4145',
'socks4://192.111.139.165:4145',
'socks4://98.170.57.249:4145',
'socks4://72.195.34.41:4145',
'socks4://198.8.94.170:4145',
'socks4://184.178.172.26:4145',
'socks4://184.185.2.12:4145',
'socks4://98.181.137.83:4145',
'socks4://68.1.210.163:4145',
'socks4://184.170.245.148:4145',
'socks4://199.58.185.9:4145',
'socks4://199.229.254.129:4145',
'socks4://46.107.230.122:1080',
'socks4://50.238.47.86:32100',
'socks4://184.178.172.13:15311',
'socks4://181.143.59.140:4153',
'socks4://174.75.211.222:4145',
'socks4://103.87.81.86:5678',
'socks4://72.195.101.99:4145',
'socks4://200.215.160.210:5678',
'socks4://177.55.191.22:60606',
'socks4://197.232.43.224:1080',
'socks4://208.65.90.21:4145',
'socks4://14.241.182.44:5678',
'socks4://199.116.112.6:4145',
'socks4://208.65.90.3:4145',
'socks4://192.111.129.150:4145',
'socks4://8.39.228.193:39593',
'socks4://200.105.252.170:5678',
'socks4://68.71.245.206:4145',
'socks4://68.71.249.158:4145',
'socks4://68.71.242.118:4145',
'socks4://72.37.216.68:4145',
'socks4://142.54.237.38:4145',
'socks4://77.225.198.220:4673',
'socks4://188.143.169.22:33333',
'socks4://69.36.63.128:1080',
'socks4://202.166.219.80:4153',
'socks4://216.68.128.121:4145',
'socks4://72.211.46.124:4145',
'socks4://139.59.24.173:1080',
'socks4://192.252.214.17:4145',
'socks4://37.52.13.164:5678',
'socks4://98.190.239.3:4145',
'socks4://115.187.50.40:5678',
'socks4://198.177.254.157:4145',
'socks4://46.8.60.34:1080',
'socks4://136.228.163.150:5678',
'socks4://184.182.240.12:4145',
'socks4://72.206.74.126:4145',
'socks4://72.223.188.92:4145',
'socks4://184.182.240.211:4145',
'socks4://98.182.171.161:4145',
'socks4://192.104.242.158:4145',
'socks4://98.191.0.47:4145',
'socks4://94.198.211.217:5678',
'socks4://93.183.175.6:5678',
'socks4://168.196.24.29:60606',
'socks4://129.205.244.185:5678',
'socks4://177.126.89.63:4145',
'socks4://113.11.183.199:4145',
'socks4://93.183.124.28:1080',
'socks4://117.216.46.148:1080',
'socks4://39.175.80.225:1080',
'socks4://27.68.169.78:1080',
'socks4://103.166.39.161:3629',
'socks4://115.69.210.60:1080',
'socks4://194.163.160.97:10808',
'socks4://123.200.5.146:57775',
'socks4://185.176.94.75:1080',
'socks4://115.23.88.118:56452',
'socks4://87.121.86.229:1080',
'socks4://178.130.47.15:8080',
'socks4://104.37.184.214:1080',
'socks4://159.65.158.30:8888',
'socks4://3.27.113.105:1080',
'socks4://43.139.118.27:10808',
'socks4://202.166.196.105:48293',
'socks4://114.134.88.74:9696',
'socks4://117.1.48.242:20077',
'socks4://117.1.48.242:20057',
'socks4://42.115.247.250:20002',
'http://84.17.47.150:9002',
'http://84.17.47.149:9002',
'http://84.17.47.148:9002',
'http://84.17.47.147:9002',
'http://84.17.47.146:9002',
'http://84.17.47.126:9002',
'http://84.17.47.125:9002',
'http://84.17.47.124:9002',
'http://141.147.9.254:443',
'http://65.108.150.56:8443',
'http://194.67.91.153:443',
'http://129.151.160.199:443',
'http://167.99.124.118:443',
'http://4.188.236.47:443',
'http://34.122.187.196:443',
'http://103.37.111.253:10086',
'http://78.28.152.113:443',
'http://206.81.26.113:443',
'http://23.88.59.163:443',
'http://51.38.191.151:443',
'http://154.65.39.7:443',
'http://154.65.39.8:443',
'http://103.37.111.253:10089',
'http://207.178.166.187:443',
'http://103.179.190.121:443',
'http://116.203.117.22:443',
'http://65.108.104.111:443',
'http://128.199.207.200:443',
'http://45.114.142.178:443',
'http://34.68.168.129:443',
'http://193.36.118.226:9443',
'http://195.114.209.50:443',
'http://138.199.35.215:9002',
'http://138.199.35.214:9002',
'http://138.199.35.213:9002',
'http://138.199.35.212:9002',
'http://138.199.35.208:9002',
'http://138.199.35.205:9002',
'http://138.199.35.204:9002',
'http://138.199.35.203:9002',
'http://138.199.35.201:9002',
'http://138.199.35.200:9002',
'http://138.199.35.198:9002',
'http://138.199.35.197:9002',
'http://138.199.35.196:9002',
'http://138.199.35.195:9002',
'http://45.92.108.112:443',
'http://89.117.55.119:443',
'http://138.199.35.199:9002',
'http://138.199.35.217:9002',
'http://167.71.166.28:8443',
'http://57.129.1.214:443',
'http://156.146.59.28:9002',
'http://156.146.59.29:9002',
'http://156.146.59.50:9002',
'http://217.69.241.186:443',
'http://162.243.95.8:443',
'http://103.62.50.130:443',
'http://103.62.50.130:9443',
'http://116.203.49.36:443',
'http://84.239.49.164:9002',
'http://156.146.59.8:9002',
'http://156.146.59.13:9002',
'http://156.146.59.2:9002',
'http://156.146.59.3:9002',
'http://156.146.59.4:9002',
'http://156.146.59.5:9002',
'http://156.146.59.6:9002',
'http://156.146.59.7:9002',
'http://156.146.59.9:9002',
'http://156.146.59.10:9002',
'http://84.239.49.37:9002',
'http://84.239.49.38:9002',
'http://84.239.49.39:9002',
'http://156.146.59.11:9002',
'http://84.239.49.40:9002',
'http://84.239.49.41:9002',
'http://84.239.49.43:9002',
'http://84.239.49.44:9002',
'http://84.239.49.45:9002',
'http://84.239.49.46:9002',
'http://84.239.49.47:9002',
'http://84.239.49.48:9002',
'http://84.239.49.49:9002',
'http://84.239.49.50:9002',
'http://156.146.59.12:9002',
'http://84.239.49.51:9002',
'http://156.146.59.14:9002',
'http://156.146.59.15:9002',
'http://156.146.59.16:9002',
'http://156.146.59.17:9002',
'http://156.146.59.18:9002',
'http://156.146.59.19:9002',
'http://156.146.59.20:9002',
'http://84.239.49.157:9002',
'http://84.239.49.161:9002',
'http://84.239.49.169:9002',
'http://84.239.49.200:9002',
'http://84.239.49.204:9002',
'http://84.239.49.209:9002',
'http://84.239.49.218:9002',
'http://84.239.49.220:9002',
'http://84.239.49.229:9002',
'http://84.239.49.231:9002',
'http://84.239.49.244:9002',
'http://84.239.49.246:9002',
'http://84.239.49.247:9002',
'http://84.239.49.248:9002',
'http://84.239.49.249:9002',
'http://84.239.49.250:9002',
'http://84.239.49.251:9002',
'http://84.239.49.253:9002',
'http://84.239.49.254:9002',
'http://84.239.14.176:9002',
'http://84.239.14.160:9002',
'http://84.239.14.146:9002',
'http://84.239.14.147:9002',
'http://84.239.14.148:9002',
'http://84.239.14.149:9002',
'http://84.239.14.150:9002',
'http://84.239.14.151:9002',
'http://84.239.14.152:9002',
'http://84.239.14.153:9002',
'http://84.239.14.154:9002',
'http://84.239.14.155:9002',
'http://84.239.14.156:9002',
'http://84.239.14.157:9002',
'http://84.239.14.158:9002',
'http://84.239.14.159:9002',
'http://84.239.14.162:9002',
'http://84.239.14.163:9002',
'http://84.239.14.164:9002',
'http://84.239.14.165:9002',
'http://84.239.14.166:9002',
'http://84.239.14.167:9002',
'http://84.239.14.168:9002',
'http://84.239.14.169:9002',
'http://84.239.14.170:9002',
'http://84.239.14.171:9002',
'http://84.239.14.172:9002',
'http://84.239.14.173:9002',
'http://84.239.14.174:9002',
'http://84.239.14.175:9002',
'http://192.73.244.36:443',
'http://51.254.213.34:443',
'http://156.232.10.14:3128',
'http://51.79.173.71:443',
'http://62.138.18.91:443',
'http://102.130.125.86:443',
    # ... add all your proxies here
]

def get_random_proxy():
    return {'http': random.choice(proxies_list), 'https': random.choice(proxies_list)}

# In your reporting function, replace the requests call with:
def send_report(report_data):
    proxy = get_random_proxy()
   
    try:
        response = requests.post(
            'https://your-reporting-endpoint.com/api/report',
            json=report_data,
            proxies=proxy,
            timeout=30
        )
        print(f"Report sent via {proxy['http']} - Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Proxy {proxy['http']} failed: {e}")
        return False
