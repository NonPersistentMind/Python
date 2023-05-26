import logging, shutil, numpy as np, os, re
from PIL import Image
from config import BOT_TOKEN
from img_processing_utils import source_folder, dest_folder
from telegram import Update, Bot
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logfile = open('.log', 'a')
log = lambda *args, **kwargs: print(*args, **kwargs, file=logfile, flush=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='.log'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # log(10, update.message.text)
    response = open('start_message.html', 'r').read()
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=response.replace('%%username%%', update.effective_user.username),
                                   parse_mode='html')
    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(10, update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=update.message.text)


async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_id = update.message.photo[-1].file_id if update.message.photo else update.message.effective_attachment.file_id
    new_file = await context.bot.get_file(image_id)
    filename = await new_file.download_to_drive()
    filename = filename.as_posix()
    
    try:
        img = np.array(Image.open(filename))
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="It doesn't seem like an image to me. \nSadly, but I can't handle anything else yet.")
        return
    
    if update.message.caption:
        # Encoding
        log('Encoding now')
        
        # Move a file to a source directory
        try:
            shutil.move(filename, source_folder)
        except shutil.Error:
            os.remove(source_folder + filename)
            shutil.move(filename, source_folder)

        # Insert the message in the image
        from numpy_img_processing import encode_image
        try:
            img = encode_image(img, update.message.caption)
        except ValueError as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>The error happened... 🤷‍♂🤷‍♂🤷‍♂</b>\n{str(e)}", parse_mode='html')
            return

        # Save resulting image in a lossless format (.png)
        dest_path = dest_folder + re.sub('\.\w+$', '.png', filename)
        with open(dest_path,'wb') as file:
            img.save(file, format='png')
        
        # Send the image back to the user
        with open(dest_path, 'rb') as imagefile:
            await context.bot.send_document(update.effective_chat.id, imagefile)
            
        # os.remove(dest_path)
    
    else:
        # Decoding
        log("Decoding now") 
        from numpy_img_processing import decode_image
        
        try:
            msg = decode_image(img)
            os.remove(filename)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        except Exception:
            os.remove(filename)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="It doesn't seem this image has any message in it that I can read")
    
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    image_handler = MessageHandler(filters.PHOTO | filters.ATTACHMENT, process_image)
    # file_handler = MessageHandler(filters.ATTACHMENT, process_attachment)
    
    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(image_handler)
    # application.add_handler(file_handler)
    
    application.run_polling()
