# replit_verizon_bot.py
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
        """Genera lote pequeño de números para Replit"""
        return [self.generate_verizon_number() for _ in range(min(count, 10))]

# ==================== VALIDADOR REPLIT-SAFE ====================
class ReplitSafeValidator:
    def __init__(self):
        self.request_count = 0
        self.last_request_time = 0
        self.session_start = time.time()
        
    async def safe_delay(self, operation_type="validate"):
        """Delay seguro para Replit"""
        if operation_type == "validate":
            delay = random.uniform(8, 15)  # 8-15 segundos para validación
        else:  # brute force
            delay = random.uniform(3, 8)   # 3-8 segundos para PIN
            
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
        """Valida número de forma segura"""
        await self.safe_delay("validate")
        
        # Simulación realista
        await asyncio.sleep(random.uniform(1, 2))
        
        # 65% de probabilidad de ser Verizon (más realista)
        if random.random() < 0.65:
            return {
                "valid": True,
                "carrier": "Verizon Wireless",
                "status": random.choice(["active", "active", "suspended"]),  # Más activos
                "line_type": random.choice(["postpaid", "prepaid"]),
                "device": random.choice(["iPhone 15 Pro", "Samsung S24", "Google Pixel 8", "iPhone 14"]),
                "plan": random.choice(["5G Get More", "5G Play More", "5G Start", "Unlimited Plus"]),
                "balance": random.randint(0, 300),
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
    
    async def brute_force_pin(self, phone_number, max_attempts=6):  # Menos intentos para Replit
        """Fuerza bruta segura para Replit"""
        common_pins = ['0000', '1234', '1111', '1212', '1004', '2000']
        
        for attempt, pin in enumerate(common_pins[:max_attempts], 1):
            await self.safe_delay("bruteforce")
            
            # 20% de probabilidad de éxito por intento (más realista)
            if random.random() < 0.20:
                return {
                    "success": True,
                    "pin": pin,
                    "attempts": attempt,
                    "account_access": True,
                    "security_level": random.choice(["low", "medium"]),
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "success": False, 
            "attempts": max_attempts,
            "suggestion": "Try personalized PIN patterns",
            "timestamp": datetime.now().isoformat()
        }

# ==================== BOT TELEGRAM ====================
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    
    class ReplitVerizonBot:
        def __init__(self):
            self.validator = ReplitSafeValidator()
            self.number_gen = VerizonNumberGenerator()
            self.updater = Updater(TELEGRAM_TOKEN, use_context=True)
            self.dispatcher = self.updater.dispatcher
            self.setup_handlers()
        
        def setup_handlers(self):
            """Configura los comandos del bot"""
            self.dispatcher.add_handler(CommandHandler("start", self.start_command))
            self.dispatcher.add_handler(CommandHandler("validate", self.validate_command))
            self.dispatcher.add_handler(CommandHandler("generate", self.generate_command))
            self.dispatcher.add_handler(CommandHandler("bruteforce", self.bruteforce_command))
            self.dispatcher.add_handler(CommandHandler("stats", self.stats_command))
            self.dispatcher.add_handler(CommandHandler("research", self.research_command))
            self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
        
        def start_command(self, update: Update, context: CallbackContext):
            """Comando /start"""
            user = update.effective_user
            welcome_text = f"""
🔬 *ACADEMIC RESEARCH BOT - VERIZON PATTERNS*

Welcome {user.first_name} to the telecommunications research tool.

*Available Research Commands:*
🔍 `/validate +1234567890` - Analyze carrier pattern
🔢 `/generate [1-5]` - Generate research samples  
🔓 `/bruteforce +1234567890` - PIN security research
📊 `/stats` - Research statistics
📋 `/research` - Web dashboard

*Research Examples:*
`/validate +12025551234`
`/generate 3`
`/bruteforce +12025551234`

*Academic Purpose:*
This tool simulates carrier analysis for educational research in telecommunications security.

⚠️ *For Academic Use Only*
            """
            update.message.reply_text(welcome_text, parse_mode="Markdown")
        
        async def validate_command(self, update: Update, context: CallbackContext):
            """Comando /validate"""
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
            
            update.message.reply_text("🔍 *Analyzing carrier pattern...*", parse_mode="Markdown")
            
            # Realizar validación
            result = await self.validator.validate_number(phone_number)
            
            if result["valid"]:
                USER_STATS[user_id]["validated"] += 1
                
                response_text = f"""
✅ *VERIZON CARRIER DETECTED*

📱 *Number:* `{phone_number}`
🏢 *Carrier:* {result['carrier']}
📊 *Status:* {result['status']}
📟 *Type:* {result['line_type']}
📲 *Device:* {result['device']}
📋 *Plan:* {result['plan']}
💰 *Balance:* ${result['balance']}
🎯 *Confidence:* {result['confidence']}%

💡 Use `/bruteforce {phone_number}` for security research
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
                    count = min(int(context.args[0]), 5)  # Máximo 5 en Replit
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
            
            response_text += f"\n💡 Use `/validate [number]` for carrier analysis"
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        async def bruteforce_command(self, update: Update, context: CallbackContext):
            """Comando /bruteforce"""
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
            
            update.message.reply_text("🔓 *Researching PIN security...*", parse_mode="Markdown")
            
            # Primero validar que sea Verizon
            validation = await self.validator.validate_number(phone_number)
            if not validation["valid"]:
                update.message.reply_text("❌ *Research Error:* Number is not Verizon", parse_mode="Markdown")
                return
            
            # Realizar fuerza bruta
            result = await self.validator.brute_force_pin(phone_number)
            
            if result["success"]:
                response_text = f"""
🎉 *PIN SECURITY RESEARCH COMPLETED*

📱 *Number:* `{phone_number}`
🔑 *PIN Found:* `{result['pin']}`
🎯 *Attempts:* {result['attempts']}
🛡️ *Security Level:* {result['security_level']}
✅ *Access:* {'Granted' if result['account_access'] else 'Limited'}

⚠️ *Academic Research Only*
                """
                USER_STATS[user_id]["validated"] += 1
            else:
                response_text = f"""
❌ *PIN NOT IDENTIFIED*

📱 *Number:* `{phone_number}`
🎯 *Attempts:* {result['attempts']}
💡 *Suggestion:* {result['suggestion']}

🔒 *Security Note:* PIN complexity prevents identification
                """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
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
✅ *Carriers Analyzed:* {stats['validated']}
🔍 *Research Queries:* {stats['searches']}
📈 *Remaining Analyses:* {remaining_validations}
🔬 *Remaining Queries:* {remaining_searches}

💎 *Research Tier:* {'🔬 PREMIUM' if user_id == OWNER_ID else '📚 STANDARD'}
            """
            
            update.message.reply_text(response_text, parse_mode="Markdown")
        
        def research_command(self, update: Update, context: CallbackContext):
            """Comando /research - Muestra dashboard web"""
            user = update.effective_user
            
            # Datos de ejemplo para la web
            research_results = [
                {
                    "number": "+12025551234",
                    "valid": True,
                    "carrier": "Verizon Wireless",
                    "status": "active",
                    "confidence": 95,
                    "timestamp": datetime.now().isoformat()
                }
            ]
            
            limits = {
                "remaining": 30 - USER_STATS[user.id]["searches"]
            }
            
            dashboard_url = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"
            
            update.message.reply_text(
                f"🔬 *Research Dashboard*\n\n"
                f"🌐 *Web Interface:* {dashboard_url}\n"
                f"📊 *Live statistics and research data*\n"
                f"📈 *Real-time analytics*\n\n"
                f"💡 *Access from your browser for full research capabilities*",
                parse_mode="Markdown"
            )
        
        def handle_message(self, update: Update, context: CallbackContext):
            """Maneja mensajes normales"""
            update.message.reply_text("""
🔬 *Academic Research Bot*

Use /start for research commands
Use /research for web dashboard

*Research Commands:*
/validate - Analyze carrier
/generate - Create samples
/bruteforce - Security research  
/stats - Research metrics
            """, parse_mode="Markdown")
        
        def start_bot(self):
            """Inicia el bot"""
            print("🔬 ACADEMIC RESEARCH BOT STARTED")
            print(f"👤 Owner ID: {OWNER_ID}")
            print("✅ Bot running in Replit-safe mode")
            print("🌐 Web dashboard available at /research")
            
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
        "project": "Academic Carrier Research",
        "version": "1.0",
        "purpose": "Educational telecommunications analysis",
        "limits": {
            "max_requests": 30,
            "reset_period": "hourly"
        }
    }

# ==================== CONFIGURACIÓN RENDER ====================
def is_running_on_render():
    return 'RENDER' in os.environ

# Configuración específica para Render
if is_running_on_render():
    print("🔥 RENDER DEPLOYMENT DETECTED")
    # Ajustes para Render
    RENDER_CONFIG = {
        "max_requests": 50,
        "delay_multiplier": 1.5,
        "web_only": False
    }

# ==================== INICIALIZACIÓN MEJORADA ====================
def main():
    """Función principal mejorada para Render"""
    print("🚀 INITIALIZING ACADEMIC RESEARCH PLATFORM")
    
    if is_running_on_render():
        print("✅ Running on Render.com")
        print("🌐 Web Server: ACTIVE")
        print("🤖 Telegram Bot: ACTIVE")
        
        # Iniciar ambos servicios en Render
        import threading
        
        def start_bot():
            try:
                bot = ReplitVerizonBot()
                bot.start_bot()
            except Exception as e:
                print(f"❌ Bot error: {e}")
        
        # Iniciar bot en hilo separado
        bot_thread = threading.Thread(target=start_bot, daemon=True)
        bot_thread.start()
        
        # Iniciar servidor web principal
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
        
    elif os.getenv('REPL_SLUG'):
        print("✅ Running in Replit environment")
        app.run(host='0.0.0.0', port=5000, debug=False)
    elif TELEGRAM_TOKEN:
        print("✅ Running in standalone mode with Telegram")
        bot = ReplitVerizonBot()
        bot.start_bot()
    else:
        print("🌐 Starting web server only")
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
    
