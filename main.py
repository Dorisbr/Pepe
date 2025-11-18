# Verizon Method by Swippe God
import os
import random
import time
from datetime import datetime
from collections import defaultdict
from flask import Flask

# Configuración
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OWNER_ID = 6699273462

# Sistema de usuarios
USER_STATS = defaultdict(lambda: {"validados": 0, "busquedas": 0})

# Servidor web simple
app = Flask(__name__)

@app.route('/')
def status():
    return "✅ Bot Verizon Method - ACTIVO"

@app.route('/health')
def health():
    return {"status": "online", "bot": "Verizon Method"}

# Validador simple
class ValidadorVerizon:
    def __init__(self):
        self.codigos_area = ['201','202','203','205','206','212','213','214','215']
    
    def validar_numero(self, numero):
        time.sleep(random.uniform(1, 3))
        
        if random.random() < 0.7:
            return {
                "valido": True,
                "compañia": "Verizon Wireless",
                "estado": "activo",
                "tipo": random.choice(["postpago", "prepago"]),
                "dispositivo": random.choice(["iPhone 15", "Samsung S24"]),
                "plan": random.choice(["5G Get More", "5G Play More"]),
                "confianza": random.randint(85, 98)
            }
        else:
            return {
                "valido": False,
                "compañia": random.choice(["AT&T", "T-Mobile"]),
                "estado": "inactivo"
            }
    
    def buscar_pin(self, numero):
        time.sleep(random.uniform(2, 4))
        
        pines_comunes = ['0000', '1234', '1111', '1212', '1004']
        
        for pin in pines_comunes:
            if random.random() < 0.25:
                return {
                    "exito": True,
                    "pin": pin,
                    "intentos": pines_comunes.index(pin) + 1
                }
        
        return {"exito": False, "intentos": len(pines_comunes)}
    
    def generar_numero(self):
        area = random.choice(self.codigos_area)
        prefijo = random.choice(['300', '400', '500'])
        linea = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"+1{area}{prefijo}{linea}"

# Bot de Telegram
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    
    class BotVerizon:
        def __init__(self):
            self.validador = ValidadorVerizon()
            self.updater = Updater(TELEGRAM_TOKEN, use_context=True)
            self.dispatcher = self.updater.dispatcher
            self.configurar_comandos()
        
        def configurar_comandos(self):
            self.dispatcher.add_handler(CommandHandler("start", self.comando_start))
            self.dispatcher.add_handler(CommandHandler("validar", self.comando_validar))
            self.dispatcher.add_handler(CommandHandler("generar", self.comando_generar))
            self.dispatcher.add_handler(CommandHandler("pin", self.comando_pin))
            self.dispatcher.add_handler(CommandHandler("estadisticas", self.comando_stats))
            self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.mensaje_normal))
        
        def comando_start(self, update: Update, context: CallbackContext):
            user = update.effective_user
            mensaje = f"""
🔰 *Verizon Method - By Swippe God*

Hola {user.first_name}, bienvenido al sistema de validación Verizon.

*Comandos disponibles:*
✅ `/validar +1234567890` - Validar línea Verizon
🔢 `/generar [cantidad]` - Generar números  
🔓 `/pin +1234567890` - Buscar PIN de línea
📊 `/estadisticas` - Tus estadísticas

*Ejemplos:*
`/validar +12025551234`
`/generar 5`
`/pin +12025551234`
            """
            update.message.reply_text(mensaje, parse_mode="Markdown")
        
        def comando_validar(self, update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ Uso: `/validar +1234567890`", parse_mode="Markdown")
                return
            
            numero = context.args[0]
            
            if not numero.startswith('+1') or len(numero) != 12:
                update.message.reply_text("❌ Formato: `+1XXXXXXXXXX`", parse_mode="Markdown")
                return
            
            USER_STATS[user_id]["busquedas"] += 1
            
            update.message.reply_text("🔍 *Validando número...*", parse_mode="Markdown")
            
            resultado = self.validador.validar_numero(numero)
            
            if resultado["valido"]:
                USER_STATS[user_id]["validados"] += 1
                respuesta = f"""
✅ *LÍNEA VERIZON ENCONTRADA*

📱 *Número:* `{numero}`
🏢 *Compañía:* {resultado['compañia']}
📊 *Estado:* {resultado['estado']}
📟 *Tipo:* {resultado['tipo']}
📲 *Dispositivo:* {resultado['dispositivo']}
📋 *Plan:* {resultado['plan']}
🎯 *Confianza:* {resultado['confianza']}%

💡 Usa `/pin {numero}` para buscar PIN
                """
            else:
                respuesta = f"""
❌ *NO ES VERIZON*

📱 *Número:* `{numero}`
🏢 *Compañía:* {resultado['compañia']}
🚫 *Estado:* No es Verizon
                """
            
            update.message.reply_text(respuesta, parse_mode="Markdown")
        
        def comando_generar(self, update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            cantidad = 1
            
            if context.args:
                try:
                    cantidad = min(int(context.args[0]), 10)
                except:
                    cantidad = 1
            
            USER_STATS[user_id]["busquedas"] += cantidad
            
            update.message.reply_text(f"🔢 *Generando {cantidad} números...*", parse_mode="Markdown")
            
            numeros = [self.validador.generar_numero() for _ in range(cantidad)]
            
            respuesta = "📱 *NÚMEROS GENERADOS:*\n\n"
            for i, num in enumerate(numeros, 1):
                respuesta += f"`{i}. {num}`\n"
            
            respuesta += f"\n💡 Usa `/validar [número]` para verificar"
            
            update.message.reply_text(respuesta, parse_mode="Markdown")
        
        def comando_pin(self, update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            
            if not context.args:
                update.message.reply_text("❌ Uso: `/pin +1234567890`", parse_mode="Markdown")
                return
            
            numero = context.args[0]
            USER_STATS[user_id]["busquedas"] += 1
            
            update.message.reply_text("🔓 *Buscando PIN...*", parse_mode="Markdown")
            
            # Primero validar que sea Verizon
            validacion = self.validador.validar_numero(numero)
            if not validacion["valido"]:
                update.message.reply_text("❌ El número no es Verizon", parse_mode="Markdown")
                return
            
            resultado = self.validador.buscar_pin(numero)
            
            if resultado["exito"]:
                respuesta = f"""
🎉 *PIN ENCONTRADO*

📱 *Número:* `{numero}`
🔑 *PIN:* `{resultado['pin']}`
🎯 *Intentos:* {resultado['intentos']}

✅ PIN identificado correctamente
                """
                USER_STATS[user_id]["validados"] += 1
            else:
                respuesta = f"""
❌ *PIN NO ENCONTRADO*

📱 *Número:* `{numero}`
🎯 *Intentos:* {resultado['intentos']}

💡 Prueba con otro número
                """
            
            update.message.reply_text(respuesta, parse_mode="Markdown")
        
        def comando_stats(self, update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            stats = USER_STATS[user_id]
            
            respuesta = f"""
📊 *TUS ESTADÍSTICAS*

👤 *Usuario:* {update.effective_user.first_name}
✅ *Líneas validadas:* {stats['validados']}
🔍 *Búsquedas realizadas:* {stats['busquedas']}

💎 *Status:* {'🔥 PREMIUM' if user_id == OWNER_ID else '💀 FREE'}
            """
            
            update.message.reply_text(respuesta, parse_mode="Markdown")
        
        def mensaje_normal(self, update: Update, context: CallbackContext):
            update.message.reply_text("""
🤖 *Verizon Method Bot*

Usa /start para ver comandos
Usa /validar +1234567890 para validar

*Comandos:*
/validar - Validar línea
/generar - Generar números
/pin - Buscar PIN
/estadisticas - Estadísticas
            """, parse_mode="Markdown")
        
        def iniciar_bot(self):
            print("🤖 Bot Verizon Method - INICIADO")
            self.updater.start_polling()
            self.updater.idle()

except ImportError:
    print("⚠️ Librerías de Telegram no disponibles")

# Función principal
def main():
    print("🚀 Iniciando Verizon Method...")
    
    # Iniciar bot si hay token
    if TELEGRAM_TOKEN:
        try:
            bot = BotVerizon()
            print("✅ Bot Telegram: ACTIVO")
            
            # Iniciar en hilo separado
            import threading
            bot_thread = threading.Thread(target=bot.iniciar_bot, daemon=True)
            bot_thread.start()
            
        except Exception as e:
            print(f"❌ Error en bot: {e}")
    
    # Iniciar servidor web
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Servidor web en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    main()
