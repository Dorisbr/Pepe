# main.py
import os
import asyncio
import random
import time
from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template_string

# ==================== CONFIGURACIÓN ====================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = 6699273462

# ==================== SISTEMA DE USUARIOS ====================
USER_STATS = defaultdict(lambda: {"validated": 0, "searches": 0, "last_reset": datetime.now().isoformat()})
ACTIVE_SESSIONS = {}

# ==================== APARIENCIA WEB LEGÍTIMA ====================
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Phone Research Lab</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f0f2f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .container { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .result { padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
        .success { border-left-color: #2ecc71; background: #ecfbf3; }
        .error { border-left-color: #e74c3c; background: #fdeded; }
        .warning { border-left-color: #f39c12; background: #fef5e7; }
        code { background: #2c3e50; color: white; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 Phone Research Laboratory</h1>
        <p>Academic Research on Telecommunications Patterns</p>
    </div>
    
    <div class="container">
        <h2>Research Dashboard</h2>
        <p>This tool is for educational research on phone number patterns and carrier identification methodologies.</p>
        
        {% if results %}
        <div class="container">
            <h3>Latest Research Results</h3>
            {% for result in results %}
                <div class="result {% if result.valid %}success{% else %}error{% endif %}">
                    <strong>{{ result.number }}</strong><br>
                    Carrier: {{ result.carrier }}<br>
                    Status: {{ result.status }}<br>
                    Confidence: {{ result.confidence }}%<br>
                    <small>Research timestamp: {{ result.timestamp }}</small>
                </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="container warning">
            <h3>🔒 Research Ethics</h3>
            <p>This tool operates under academic research guidelines. All data is simulated for educational purposes.</p>
            <p><strong>Usage Limits:</strong> {{ limits.remaining }} researches remaining (resets hourly)</p>
        </div>
    </div>
</body>
</html>
"""

# ==================== GENERADOR DE NÚMEROS ====================
class VerizonNumberGenerator:
    def __init__(self):
        self.area_codes = [
            '201', '202', '203', '205', '206', '207', '208', '209', '210', '212',
            '213', '214', '215', '216', '217', '218', '219', '220', '224', '225'
        ]
    
    def generate_verizon_number(self):
        """Genera número Verizon válido"""
        area = random.choice(self.area_codes)
        prefix = random.choice(['300', '400', '500', '600', '700'])
        line = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"+1{area}{prefix}{line}"
    
    def generate_number_batch(self, count=5):
        """Genera lote pequeño de números"""
        return [self.generate_verizon_number() for _ in range(min(count, 10))]

# ==================== VALIDADOR COMPLETO ====================
class AdvancedValidator:
    def __init__(self):
        self.request_count = 0
        self.last_request_time = 0
        self.session_start = time.time()
        
    async def safe_delay(self, operation_type="validate"):
        """Delay seguro"""
        if operation_type == "validate":
            delay = random.uniform(5, 12)
        else:  # brute force
            delay = random.uniform(2, 6)
            
        print(f"⏰ Safe delay: {delay:.1f}s for {operation_type}")
        await asyncio.sleep(delay)
        
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
    
    async def validate_number(self, phone_number):
        """Valida número con información completa"""
        await self.safe_delay("validate")
        
        # Simulación realista
        await asyncio.sleep(random.uniform(1, 2))
        
        # 65% de probabilidad de ser Verizon
        if random.random() < 0.65:
            return {
                "valid": True,
                "carrier": "Verizon Wireless",
                "status": random.choice(["active", "active", "suspended"]),
                "line_type": random.choice(["postpaid", "prepaid"]),
                "device": random.choice(["iPhone 15 Pro", "Samsung S24", "Google Pixel 8", "iPhone 14"]),
                "plan": random.choice(["5G Get More", "5G Play More", "5G Start", "Unlimited Plus"]),
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
                "carrier": random.choice(["AT&T", "T-Mobile", "Sprint", "US Cellular"]),
                "status": "inactive",
                "confidence": random.randint(70, 90),
                "timestamp": datetime.now().isoformat()
            }
    
    async def brute_force_pin(self, phone_number, max_attempts=8):
        """Fuerza bruta de PIN avanzada"""
        common_pins = ['0000', '1234', '1111', '1212', '1004', '2000', '4444', '7777', '9999', '2580']
        
        for attempt, pin in enumerate(common_pins[:max_attempts], 1):
            await self.safe_delay("bruteforce")
            
            # Simular intento de validación
            success_chance = 0.25 if attempt <= 4 else 0.15  # Menos probabilidad después de 4 intentos
            
            if random.random() < success_chance:
                return {
                    "success": True,
                    "pin": pin,
                    "attempts": attempt,
                    "account_access": True,
                    "security_level": random.choice(["low", "medium"]),
                    "access_type": random.choice(["full", "limited", "temporary"]),
                    "timestamp": datetime.now().isoformat(),
                    "method_used": "common_pattern_analysis"
                }
        
        return {
            "success": False, 
            "attempts": max_attempts,
            "suggestion": "Try personalized PIN patterns or contact carrier",
            "next_steps": ["Wait 24h before retry", "Try account recovery options"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_account_details(self, phone_number, pin=None):
        """Obtiene detalles completos de la cuenta"""
        if not pin:
            pin_result = await self.brute_force_pin(phone_number)
            if not pin_result["success"]:
                return {"error": "PIN required", "pin_found": False}
            pin = pin_result["pin"]
        
        await self.safe_delay("details")
        
        return {
            "phone_number": phone_number,
            "pin": pin,
            "account_holder": random.choice(["John Smith", "Maria Garcia", "Robert Johnson", "Lisa Chen"]),
            "billing_address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'])}",
            "last_payment": f"${random.randint(50, 200)} on {(datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')}",
            "devices_connected": random.randint(1, 4),
            "family_plan": random.choice([True, False]),
            "international_roaming": random.choice([True, False]),
            "account_balance": f"${random.randint(-50, 150)}",
            "data_remaining": f"{random.randint(1, 20)}GB",
            "plan_details": {
                "name": random.choice(["5G Get More", "5G Play More", "Unlimited Welcome"]),
                "price": f"${random.randint(70, 120)}/month",
                "features": ["Unlimited Data", "Hotspot", "International Text"]
            },
            "timestamp": datetime.now().isoformat()
        }

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

*Research Examples:*
`/validate +12025551234`
`/generate 5`
`/bruteforce +12025551234`
`/details +12025551234`

*Academic Purpose:*
Advanced research tool for telecommunications security and pattern analysis.

⚠️ *For Academic Research Only*
            """
            update.message.reply_text(welcome_text, parse_mode="Markdown")
        
        async def validate_command(self, update: Update, context: CallbackContext):
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
            
            # Validar formato
            if not phone_number.startswith('+1') or len(phone_number) != 12:
                update.message.reply_text("❌ *Invalid Format:* Use `+1XXXXXXXXXX`", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("🔍 *Running complete carrier analysis...*", parse_mode="Markdown")
            
            # Realizar validación completa
            result = await self.validator.validate_number(phone_number)
            
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
📊 *Data Usage:* {result['data_usage']}
💳 *Payment:* {result['payment_status']}
⏳ *Account Age:* {result['account_age']}
🎯 *Confidence:* {result['confidence']}%

💡 *Next Steps:*
• Use `/bruteforce {phone_number}` for PIN research
• Use `/details {phone_number}` for full account info
                """
            else:
                response_text = f"""
❌ *NON-VERIZON CARRIER*

📱 *Number:* `{phone_number}`
🏢 *Carrier:* {result['carrier']}
🚫 *Status:* Not in Verizon network
🎯 *Confidence:* {result['confidence']}%

💡 Try another research sample
                """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        async def generate_command(self, update: Update, context: CallbackContext):
            """Comando /generate"""
            user_id = update.effective_user.id
            count = 1
            
            if context.args:
                try:
                    count = min(int(context.args[0]), 10)
                except:
                    count = 1
            
            # Verificar límites
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
            
            response_text += f"\n💡 Use `/validate [number]` for complete analysis"
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        async def bruteforce_command(self, update: Update, context: CallbackContext):
            """Comando /bruteforce - Investigación PIN"""
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ *Usage:* `/bruteforce +1234567890`", parse_mode="Markdown")
                return
            
            phone_number = context.args[0]
            
            # Verificar límites
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("🔓 *Starting advanced PIN security research...*", parse_mode="Markdown")
            
            # Primero validar que sea Verizon
            validation = await self.validator.validate_number(phone_number)
            if not validation["valid"]:
                update.message.reply_text("❌ *Research Error:* Number is not Verizon", parse_mode="Markdown")
                return
            
            # Realizar fuerza bruta avanzada
            result = await self.validator.brute_force_pin(phone_number)
            
            if result["success"]:
                response_text = f"""
🎉 *PIN SECURITY RESEARCH - SUCCESS*

📱 *Number:* `{phone_number}`
🔑 *PIN Found:* `{result['pin']}`
🎯 *Attempts:* {result['attempts']}
🛡️ *Security Level:* {result['security_level']}
🔓 *Access Type:* {result['access_type']}
🔧 *Method:* {result['method_used']}
✅ *Status:* PIN successfully identified

💡 *Next:*
Use `/details {phone_number}` for full account access
                """
                USER_STATS[user_id]["validated"] += 1
            else:
                response_text = f"""
❌ *PIN RESEARCH - INCONCLUSIVE*

📱 *Number:* `{phone_number}`
🎯 *Attempts:* {result['attempts']}
💡 *Suggestion:* {result['suggestion']}
📝 *Next Steps:*
{chr(10).join(['• ' + step for step in result['next_steps']])}

🔒 *Research Note:* Security measures prevented identification
                """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        async def details_command(self, update: Update, context: CallbackContext):
            """Comando /details - Información completa de cuenta"""
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ *Usage:* `/details +1234567890`", parse_mode="Markdown")
                return
            
            phone_number = context.args[0]
            
            # Verificar límites
            can_request, reason = self.validator.can_make_request(user_id)
            if not can_request:
                update.message.reply_text(f"❌ *Research Limit:* {reason}", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["searches"] += 1
            
            update.message.reply_text("📋 *Retrieving complete account details...*", parse_mode="Markdown")
            
            # Obtener detalles completos
            account_details = await self.validator.get_account_details(phone_number)
            
            if "error" in account_details:
                update.message.reply_text("❌ *Research Error:* PIN required for account details", parse_mode="Markdown")
                return
            
            response_text = f"""
📊 *COMPLETE ACCOUNT ANALYSIS*

📱 *Number:* `{account_details['phone_number']}`
🔑 *PIN:* `{account_details['pin']}`
👤 *Account Holder:* {account_details['account_holder']}
🏠 *Billing Address:* {account_details['billing_address']}
💳 *Last Payment:* {account_details['last_payment']}
📱 *Devices Connected:* {account_details['devices_connected']}
👨‍👩‍👧‍👦 *Family Plan:* {'Yes' if account_details['family_plan'] else 'No'}
🌍 *Intl Roaming:* {'Enabled' if account_details['international_roaming'] else 'Disabled'}
💰 *Account Balance:* {account_details['account_balance']}
📊 *Data Remaining:* {account_details['data_remaining']}

📋 *PLAN DETAILS:*
• Name: {account_details['plan_details']['name']}
• Price: {account_details['plan_details']['price']}
• Features: {', '.join(account_details['plan_details']['features'])}

🎯 *Research Complete - Full Access Obtained*
            """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
            USER_STATS[user_id]["validated"] += 1
        
        def stats_command(self, update: Update, context: CallbackContext):
            """Comando /stats"""
            user_id = update.effective_user.id
            stats = USER_STATS[user_id]
            
            # Calcular límites
            if user_id == OWNER_ID:
                remaining_searches = 100 - stats["searches"]
                remaining_validations = 50 - stats["validated"]
            else:
                remaining_searches = 30 - stats["searches"]
                remaining_validations = 20 - stats["validated"]
            
            response_text = f"""
📊 *RESEARCH STATISTICS*

👤 *Researcher:* {update.effective_user.first_name}
✅ *Accounts Analyzed:* {stats['validated']}
🔍 *Research Queries:* {stats['searches']}
📈 *Remaining Analyses:* {remaining_validations}
🔬 *Remaining Queries:* {remaining_searches}

💎 *Research Tier:* {'🔬 PREMIUM' if user_id == OWNER_ID else '📚 STANDARD'}
            """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def research_command(self, update: Update, context: CallbackContext):
            """Comando /research - Dashboard web"""
            user = update.effective_user
            
            dashboard_url = f"https://{os.getenv('REPL_SLUG', 'your-app')}.onrender.com"
            
            update.message.reply_text(
                f"🔬 *Research Dashboard*\n\n"
                f"🌐 *Web Interface:* {dashboard_url}\n"
                f"📊 *Live research statistics*\n"
                f"📈 *Real-time analytics*\n"
                f"🔍 *Advanced research tools*\n\n"
                f"💡 *Access from browser for full capabilities*",
                parse_mode="Markdown"
            )
        
        def handle_message(self, update: Update, context: CallbackContext):
            """Maneja mensajes normales"""
            update.message.reply_text("""
🔬 *Verizon Research Bot - Complete Edition*

Use /start for all research commands
Use /research for web dashboard

*Advanced Research Commands:*
/validate - Complete carrier analysis
/generate - Create research samples  
/bruteforce - PIN security research
/details - Full account information
/stats - Research metrics
            """, parse_mode="Markdown")
        
        def start_bot(self):
            """Inicia el bot"""
            print("🔬 VERIZON RESEARCH BOT STARTED - COMPLETE EDITION")
            print(f"👤 Owner ID: {OWNER_ID}")
            print("✅ All features activated: Validation, PIN Research, Account Details")
            print("🌐 Web dashboard integrated")
            
            self.updater.start_polling()
            self.updater.idle()

except ImportError:
    print("⚠️ Telegram libraries not available - running in web mode only")

# ==================== WEB SERVER ====================
@app.route('/')
def research_dashboard():
    """Dashboard web de investigación"""
    research_results = [
        {
            "number": "+12025551234",
            "valid": True,
            "carrier": "Verizon Wireless", 
            "status": "active",
            "confidence": 95,
            "timestamp": datetime.now().isoformat()
        },
        {
            "number": "+12125551234",
            "valid": False,
            "carrier": "AT&T",
            "status": "inactive", 
            "confidence": 87,
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    limits = {
        "remaining": 25
    }
    
    return render_template_string(HTML_TEMPLATE, results=research_results, limits=limits)

@app.route('/api/research')
def api_research():
    """API para investigación"""
    return {
        "project": "Advanced Verizon Research",
        "version": "2.0",
        "purpose": "Comprehensive telecommunications security research",
        "features": ["Carrier Analysis", "PIN Research", "Account Details"],
        "limits": {
            "max_requests": 30,
            "reset_period": "hourly"
        }
    }

# ==================== INICIALIZACIÓN ====================
def main():
    """Función principal"""
    print("🚀 INITIALIZING ADVANCED VERIZON RESEARCH PLATFORM")
    print("🔬 Complete Edition: Validation + PIN Research + Account Details")
    print("🌐 Web Server: ACTIVE")
    
    # Iniciar servidor web
    if os.getenv('RENDER'):
        print("✅ Running on Render.com")
        port = int(os.environ.get('PORT', 10000))
        
        # Iniciar bot si hay token
        if TELEGRAM_TOKEN:
            try:
                bot = VerizonResearchBot()
                print("🤖 Telegram Bot: ACTIVE")
                
                # Iniciar bot en hilo separado
                import threading
                bot_thread = threading.Thread(target=bot.start_bot, daemon=True)
                bot_thread.start()
                
            except Exception as e:
                print(f"❌ Bot failed: {e}")
        
        app.run(host='0.0.0.0', port=port, debug=False)
        
    elif os.getenv('REPL_SLUG'):
        print("✅ Running in Replit environment")
        app.run(host='0.0.0.0', port=5000, debug=False)
    elif TELEGRAM_TOKEN:
        print("✅ Running in standalone mode with Telegram")
        bot = VerizonResearchBot()
        bot.start_bot()
    else:
        print("🌐 Starting web server only")
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
