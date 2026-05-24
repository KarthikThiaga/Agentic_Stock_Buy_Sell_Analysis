from app.ui import StreamlitUIDisplay

StreamlitUI = StreamlitUIDisplay()

def emit_event(message):
    if message['type'] == 'info':
        StreamlitUI.ui_info(message.get('text',''))
    
    if message['type'] == 'error':
        StreamlitUI.ui_error(message.get('text',''))
    
    if message['type'] == 'success':
        StreamlitUI.ui_success(message.get('text',''))
    
    if message['type'] == 'warning':
        StreamlitUI.ui_warning(message.get('text',''))

    if message['type'] == 'exception':
        StreamlitUI.ui_exception(message.get('text',''))

    if message['type'] == 'spinner':
        StreamlitUI.ui_spinner(message.get('text',''))   
    
    if message['type'] == 'progress':
        StreamlitUI.ui_progress_bar(0)  

    if message['type'] == 'output':
        StreamlitUI.ui_success(message.get('text',''))