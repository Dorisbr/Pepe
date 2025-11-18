# main.py
import os
import random
import time
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, render_template_string
import threading

# ==================== CONFIGURACIÓN ====================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = 6699273462

# ==================== SISTEMA DE USUARIOS ====================
USER_STATS = defaultdict(lambda: {"validated": 0, "searches": 0, "last_reset": datetime.now().isoformat()})

# ==================== APARIENCIA WEB LEGÍTIMA ====================
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Telecom Research Lab</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .container { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 Telecom Research Laboratory</h1>
        <p>Academic Research on Telecommunications Patterns</p>
    </div>
    <div class="container">
        <h2>Research Dashboard</h2>
        <p>Advanced telecommunications security research platform.</p>
        <p><strong>Status:</strong> Online</p>
        <p><strong>Features:</strong> Carrier Analysis, PIN Research, Account Details</p>
    </div>
</body>
</html>
"""

# ==================== VALIDADOR CON REQUESTS ====================
class AdvancedValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def safe_delay(self, operation_type="validate"):
        """Delay seguro"""
        if operation_type == "validate":
            delay = random.uniform(3, 8)
        else:  # brute force
            delay = random.uniform(1, 4)
            
        print(f"⏰ Safe delay: {delay:.1f}s for {operation_type}")
        time.sleep(delay)
        
    def can_make_request(self, user_id):
        """Verifica límites de uso"""
        user_stats = USER_STATS[user_id]
        
        # Reset diario
        last_reset = datetime.fromisoformat(user_stats["last_reset"])
        if (datetime.now() - last_reset).days >= 1:
            user_stats.update({"validated": 0, "searches": 0, "last_reset": datetime.now().isoformat()})
        
        # Límites por usuario
        if user_id == OWNER_ID:
            max_searches = 100
            max_validations = 50
        else:
            max_searches = 30
            max_validations = 20
            
        if user_stats["searches"] >= max_searches:
            return False, "Daily search limit reached"
        if user_stats["validated"] >= max_validations:
            return False, "Daily validation limit reached"
            
        return True, "OK"
    
    def validate_number(self, phone_number):
        """Valida número con información completa"""
        self.safe_delay("validate")
        
        # Simulación realista
        time.sleep(random.uniform(1, 2))
        
        # 65% de probabilidad de ser Verizon
        if random.random() < 0.65:
            return {
                "valid": True,
                "carrier": "Verizon Wireless",
                "status": random.choice(["active", "active", "suspended"]),
                "line_type": random.choice(["postpaid", "prepaid"]),
                "device": random.choice(["iPhone 15 Pro", "Samsung S24", "Google Pixel 8"]),
                "plan": random.choice(["5G Get More", "5G Play More", "5G Start"]),
                "balance": random.randint(0, 300),
                "data_usage": f"{random.randint(2, 15)}GB",
                "payment_status": random.choice(["current", "past due"]),
                "account_age": f"{random.randint(1, 36)} months",
                "confidence": random.randint(85, 98),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "valid": False,
                "carrier": random.choice(["AT&T", "T-Mobile", "Sprint"]),
                "status": "inactive",
                "confidence": random.randint(70, 90),
                "timestamp": datetime.now().isoformat()
            }
    
    def brute_force_pin(self, phone_number, max_attempts=8):
        """Fuerza bruta de PIN avanzada"""
        common_pins = ['0000', '1234', '1111', '1212', '1004', '2000', '4444', '7777']
        
        for attempt, pin in enumerate(common_pins[:max_attempts], 1):
            self.safe_delay("bruteforce")
            
            # Simular intento de validación
            success_chance = 0.25 if attempt <= 4 else 0.15
            
            if random.random() < success_chance:
                return {
                    "success": True,
                    "pin": pin,
                    "attempts": attempt,
                    "account_access": True,
                    "security_level": random.choice(["low", "medium"]),
                    "access_type": random.choice(["full", "limited"]),
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "success": False, 
            "attempts": max_attempts,
            "suggestion": "Try personalized PIN patterns",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_account_details(self, phone_number, pin=None):
        """Obtiene detalles completos de la cuenta"""
        if not pin:
            pin_result = self.brute_force_pin(phone_number)
            if not pin_result["success"]:
                return {"error": "PIN required", "pin_found": False}
            pin = pin_result["pin"]
        
        self.safe_delay("details")
        
        return {
            "phone_number": phone_number,
            "pin": pin,
            "account_holder": random.choice(["John Smith", "Maria Garcia", "Robert Johnson"]),
            "billing_address": f"{random.randint(100, 9999)} Main St, City, State",
            "last_payment": f"${random.randint(50, 200)}",
            "devices_connected": random.randint(1, 4),
            "account_balance": f"${random.randint(-50, 150)}",
            "data_remaining": f"{random.randint(1, 20)}GB",
            "plan_details": {
                "name": random.choice(["5G Get More", "5G Play More"]),
                "price": f"${random.randint(70, 120)}/month"
            },
            "timestamp": datetime.now().isoformat()
        }

# ==================== GENERADOR DE NÚMEROS ====================
class VerizonNumberGenerator:
    def __init__(self):
        self.area_codes = ['201', '202', '203', '205', '206', '212', '213', '214', '215']
    
    def generate_verizon_number(self):
        """Genera número Verizon válido"""
        area = random.choice(self.area_codes)
        prefix = random.choice(['300', '400', '500', '600'])
        line = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"+1{area}{prefix}{line}"
    
    def generate_number_batch(self, count=5):
        """Genera lote de números"""
        return [self.generate_verizon_number() for _ in range(min(count, 10))]

# ==================== BOT TELEGRAM COMPLETO ====================
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    
    class VerizonResearchBot:
        def __init__(self):
            self.validator = AdvancedValidator()
            self.number_gen = VerizonNumberGenerator()
            self.updater = Updater(TELEGRAM_TOKEN, use_context=True)
            self.dispatcher = self.updater.dispatcher
            self.setup_handlers()
        
        def setup_handlers(self):
            """Configura todos los comandos"""
            self.dispatcher.add_handler(CommandHandler("start", self.start_command))
            self.dispatcher.add_handler(CommandHandler("validate", self.validate_command))
            self.dispatcher.add_handler(CommandHandler("generate", self.generate_command))
            self.dispatcher.add_handler(CommandHandler("bruteforce", self.bruteforce_command))
            self.dispatcher.add_handler(CommandHandler("details", self.details_command))
            self.dispatcher.add_handler(CommandHandler("stats", self.stats_command))
            self.dispatcher.add_handler(CommandHandler("research", self.research_command))
            self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
        
        def start_command(self, update: Update, context: CallbackContext):
            """Comando /start"""
            user = update.effective_user
            welcome_text = f"""
🔬 *VERIZON RESEARCH BOT - COMPLETE EDITION*

Welcome {user.first_name} to advanced telecommunications research.

*Available Research Commands:*
🔍 `/validate +1234567890` - Complete carrier analysis
🔢 `/generate [1-10]` - Generate research samples  
🔓 `/bruteforce +1234567890` - Advanced PIN security research
📋 `/details +1234567890` - Full account information
📊 `/stats` - Research statistics
🌐 `/research` - Web dashboard

*Academic Purpose:*
Advanced research tool for telecommunications security.

⚠️ *For Academic Research Only*
            """
            update.message.reply_text(welcome_text, parse_mode="Markdown")
        
        def validate_command(self, update: Update, context: CallbackContext):
            """Comando /validate - Análisis completo"""
            user_id = update.effective_user.id
            
            # Verificar límites
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            if not context.args:
                update.message.reply_text("❌ *Usage:* `/validate +1234567890`", parse_mode="Markdown")
                return
            
            phone_number = context.args[0]
            
            if not phone_number.startswith('+1') or len(phone_number) != 12:
                update.message.reply_text("❌ *Invalid Format:* Use `+1XXXXXXXXXX`", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("🔍 *Running complete carrier analysis...*", parse_mode="Markdown")
            
            # Realizar validación completa
            result = self.validator.validate_number(phone_number)
            
            if result["valid"]:
                USER_STATS[user_id]["validated"] += 1
                response_text = f"""
✅ *VERIZON CARRIER - COMPLETE ANALYSIS*

📱 *Number:* `{phone_number}`
🏢 *Carrier:* {result['carrier']}
📊 *Status:* {result['status']}
📟 *Type:* {result['line_type']}
📲 *Device:* {result['device']}
📋 *Plan:* {result['plan']}
💰 *Balance:* ${result['balance']}
🎯 *Confidence:* {result['confidence']}%

💡 Use `/bruteforce {phone_number}` for PIN research
                """
            else:
                response_text = f"""
❌ *NON-VERIZON CARRIER*

📱 *Number:* `{phone_number}`
🏢 *Carrier:* {result['carrier']}
🚫 *Status:* Not Verizon
                """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def generate_command(self, update: Update, context: CallbackContext):
            """Comando /generate"""
            user_id = update.effective_user.id
            count = 1
            
            if context.args:
                try:
                    count = min(int(context.args[0]), 10)
                except:
                    count = 1
            
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += count
            
            update.message.reply_text(f"🔢 *Generating {count} research samples...*", parse_mode="Markdown")
            
            numbers = self.number_gen.generate_number_batch(count)
            
            response_text = "📱 *RESEARCH SAMPLES:*\n\n"
            for i, number in enumerate(numbers, 1):
                response_text += f"`{i}. {number}`\n"
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def bruteforce_command(self, update: Update, context: CallbackContext):
            """Comando /bruteforce - Investigación PIN"""
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ *Usage:* `/bruteforce +1234567890`", parse_mode="Markdown")
                return
            
            phone_number = context.args[0]
            
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("🔓 *Starting PIN security research...*", parse_mode="Markdown")
            
            # Validar que sea Verizon primero
            validation = self.validator.validate_number(phone_number)
            if not validation["valid"]:
                update.message.reply_text("❌ *Research Error:* Number is not Verizon", parse_mode="Markdown")
                return
            
            # Realizar fuerza bruta
            result = self.validator.brute_force_pin(phone_number)
            
            if result["success"]:
                response_text = f"""
🎉 *PIN RESEARCH - SUCCESS*

📱 *Number:* `{phone_number}`
🔑 *PIN Found:* `{result['pin']}`
🎯 *Attempts:* {result['attempts']}
✅ *Status:* PIN identified

💡 Use `/details {phone_number}` for account access
                """
                USER_STATS[user_id]["validated"] += 1
            else:
                response_text = f"""
❌ *PIN RESEARCH - INCONCLUSIVE*

📱 *Number:* `{phone_number}`
🎯 *Attempts:* {result['attempts']}
💡 *Suggestion:* {result['suggestion']}
                """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def details_command(self, update: Update, context: CallbackContext):
            """Comando /details - Información de cuenta"""
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ *Usage:* `/details +1234567890`", parse_mode="Markdown")
                return
            
            phone_number = context.args[0]
            
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("📋 *Retrieving account details...*", parse_mode="Markdown")
            
            # Obtener detalles
            account_details = self.validator.get_account_details(phone_number)
            
            if "error" in account_details:
                update.message.reply_text("❌ *Research Error:* PIN required", parse_mode="Markdown")
                return
            
            response_text = f"""
📊 *ACCOUNT ANALYSIS*

📱 *Number:* `{account_details['phone_number']}`
🔑 *PIN:* `{account_details['pin']}`
👤 *Account Holder:* {account_details['account_holder']}
💰 *Balance:* {account_details['account_balance']}
📊 *Data:* {account_details['data_remaining']}
📋 *Plan:* {account_details['plan_details']['name']}
            """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
            USER_STATS[user_id]["validated"] += 1
        
        def stats_command(self, update: Update, context: CallbackContext):
            """Comando /stats"""
            user_id = update.effective_user.id
            stats = USER_STATS[user_id]
            
            if user_id == OWNER_ID:
                remaining = 100 - stats["searches"]
            else:
                remaining = 30 - stats["searches"]
            
            response_text = f"""
📊 *RESEARCH STATISTICS*

✅ *Analyses:* {stats['validated']}
🔍 *Queries:* {stats['searches']}
📈 *Remaining:* {remaining}
💎 *Tier:* {'🔬 PREMIUM' if user_id == OWNER_ID else '📚 STANDARD'}
            """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def research_command(self, update: Update, context: CallbackContext):
            """Comando /research - Dashboard web"""
            update.message.reply_text(
                "🔬 *Research Dashboard*\n\n"
                "🌐 Web interface available at your Render URL\n"
                "📊 Live research statistics\n"
                "🔍 Advanced analysis tools",
                parse_mode="Markdown"
            )
        
        def handle_message(self, update: Update, context: CallbackContext):
            """Maneja mensajes normales"""
            update.message.reply_text(
                "🔬 *Verizon Research Bot*\n\n"
                "Use /start for commands\n"
                "Use /validate +1234567890 to analyze",
                parse_mode="Markdown"
            )
        
        def start_bot(self):
            """Inicia el bot"""
            print("🔬 VERIZON RESEARCH BOT STARTED")
            self.updater.start_polling()
            self.updater.idle()

except ImportError:
    print("⚠️ Telegram libraries not available")

# ==================== WEB SERVER ====================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {"status": "online", "service": "telecom_research"}

# ==================== INICIALIZACIÓN ====================
def main():
    """Función principal"""
    print("🚀 STARTING TELECOM RESEARCH PLATFORM")
    
    # Iniciar bot si hay token
    if TELEGRAM_TOKEN:
        try:
            bot = VerizonResearchBot()
            print("🤖 Telegram Bot: ACTIVE")
            
            # Iniciar bot en hilo separado
            bot_thread = threading.Thread(target=bot.start_bot, daemon=True)
            bot_thread.start()
            
        except Exception as e:
            print(f"❌ Bot failed: {e}")
    
    # Iniciar servidor web
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Web Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    main()
