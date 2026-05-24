import streamlit as st

def display_ui():
    st.title("Agentic AI for Stock Queries")
    st.header("Enter your stock related query below:")

    query = st.text_input('Please free to type in your stock related queries:', placeholder='e.g. What is the current price and news for Apple?')
    return query


class StreamlitUIDisplay:   
    def __init__(self):
        self.container = st.empty()

    def write(self, message):
        with self.container:
            st.write(message)

    def ui_error(self,text):
        with self.container:
            st.error(text)  

    def ui_success(self,text):
        with self.container:
            st.success(text)

    def ui_info(self,text):
        with self.container:
            st.info(text)

    def ui_warning(self,text):
        with self.container:
            st.warning(text)

    def ui_exception(self,text):
        with self.container:
            st.exception(text)

    def ui_spinner(self,text):
        return st.spinner(text)

    def ui_progress_bar(self,progress):
        return st.progress(progress)    

    def ui_subheader(self,text):
        with self.container:
            st.subheader(text)  

    def ui_header(self,text):    
        with self.container:
            st.header(text) 

    def ui_title(self,text):
        with self.container:
            st.title(text)  

    def ui_markdown(self,text):
        with self.container:
            st.markdown(text)   

    def ui_latex(self,text):
        with self.container:
            st.latex(text)  

    def ui_code(self,text, language='python'):
        with self.container:
            st.code(text, language=language)

    def ui_json(self,data):
        with self.container:
            st.json(data)   

    def ui_table(self,data):
        with self.container:
            st.table(data)  

    def ui_button(self,label):
        return st.button(label)

    def ui_checkbox(self,label): 
        with self.container:
            return st.checkbox(label)

    def ui_selectbox(self,label, options):
        with self.container:
            return st.selectbox(label, options)

