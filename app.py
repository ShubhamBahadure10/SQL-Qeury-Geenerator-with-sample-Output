import streamlit as st
import google.generativeai as genai
import os



os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("SQL Query Generator")
model = genai.GenerativeModel('gemini-pro')

def main():
    
    st.write("Hello! I am your SQL Query Generator. I will help you to generate a query from provided prompt")

text_input= st.text_area("Enter your query: ")

submit = st.button("Generate SQL Query")
if submit:
    with st.spinner("Generating SQL Query.."):
        template = """
                create SQL query using below text:
                '''
                {text_input}
                
                '''

    
        """
        formatted_template = template.format(text_input=text_input)
        
        response = model. generate_content(formatted_template)
        sql_query = response.text
        

        sql_query = sql_query.strip().lstrip("```sql").rstrip("``` ")

        expected_output = """
            what would be the expected output of this SQL Query:
            '''
                {sql_query}
            '''
            provide sample tabular response       
        
        """
     
        expected_output_formatted = expected_output.format(sql_query=sql_query)
        expected_output= model.generate_content(expected_output_formatted)
        expected_output=expected_output.text

        explanation = """
            explain this SQL Query:
            '''
                {sql_query}
            '''
            please provide the simple explanation       
        
        """

        explanation_formatted = explanation.format(sql_query=sql_query)
        explanation = model.generate_content(explanation_formatted)
        explanation= explanation.text
        st.write(explanation)

        with st.container():
            st.success("SQL Query Generated successfully! Hear is youe query below: ")
            st.code(sql_query, language="sql")

            st.success("Expected Output of this SQL Query will be: ")
            st.markdown(expected_output)

            st.success("Explanation of this SQL Query: ")
            st.markdown(explanation)