import requests
import logging

logger = logging.getLogger(__name__)

GREEN_API_INSTANCE = "710722702271"  # ID инстанции
GREEN_API_TOKEN = "c0fa20774e964c3ca4137760941097c3412b1fd72127455e98"  # токен аккаунта
ADMIN_WHATSAPP_NUMBER = "996774021811"  # номер телефона (куда слать уведомления)

def send_booking_to_whatsapp(reservation):
    """
    Отправляет детали бронирования администратору на WhatsApp
    """
    # Формируем URL для отправки текстового сообщения
    url = f"https://green-api.com{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
    
    # Форматируем красивый текст сообщения
    message_text = (
        "🔔 *Новое бронирование стола!* 🔔\n\n"
        f"👤 *Имя гостя:* {reservation.name}\n"
        f"📅 *Дата:* {reservation.date.strftime('%d.%m.%Y')}\n"
        f"⏰ *Время:* {reservation.time.strftime('%H:%M')}\n"
        f"👥 *Количество гостей:* {reservation.guests} чел.\n"
    )
    
    # Если гость оставил комментарий, добавляем его
    if getattr(reservation, 'comment', None):
        message_text += f"💬 *Комментарий:* _{reservation.comment}_\n"
        
    payload = {
        # Формат chatId для Green API требует суффикс @c.us для личных номеров
        "chatId": f"{ADMIN_WHATSAPP_NUMBER}@c.us",
        "message": message_text
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            logger.info("Уведомление о бронировании успешно отправлено в WhatsApp.")
            return True
        else:
            logger.error(f"Ошибка Green API: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logger.error(f"Не удалось связаться с сервером WhatsApp API: {e}")
        
    return False
