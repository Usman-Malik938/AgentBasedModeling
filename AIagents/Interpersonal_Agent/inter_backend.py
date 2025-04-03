from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient  # Correct import

app = Flask(__name__)



# Initialize            API keys
groq_api_key = "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"
tavily_api_key = "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"

# Initialize AI models
llm1 = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")  # Answer model
llm2 = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")  # Evaluation model

# Initialize Tavily API
tavily = TavilyClient(api_key=tavily_api_key)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_idea = data.get('idea', '')

    if not user_idea:
        return jsonify({"error": "user idea is required"}), 400


    prompt_template = ChatPromptTemplate.from_template("""
        ## Persona
        You are a supportive and motivational idea evaluator. Your goal is to provide constructive feedback that encourages creativity and improvement but also response on unclear user input idea.

        ## Context
        A user has submitted an idea that they would like you to evaluate. Your feedback should be tailored to the clarity and quality of the idea presented.

        ## Forced Instructions
        - If the idea is **unclear** or **unrealistic**, respond with: "The idea entered does not make sense. Please try again with a clearer concept!"
        - If the idea is straightforward but lacks detail, encourage the user by saying: "This is a good starting point! Consider adding more details to enhance your idea."
        - Always maintain a positive and encouraging tone in your feedback.
        - **Limit your response to a maximum of 4 lines. Concisely summarize your feedback.**

        ## Idea
        {idea}

        ## Response Format
        - Keep your response within four lines.
        - Avoid unnecessary details; be concise and constructive.
    """)

#        - There can be slight increase and decrease in number of bullet points in each call



    prompt = prompt_template.format(idea=user_idea)

    try:
        response = llm1.invoke(prompt)
        ai_response = response.content.strip()
    except Exception as e:
        return jsonify({"error": f"AI Response Failed: {str(e)}"}), 500

   


    # === Step 4: Return JSON Response ===
    return jsonify({
        "response": ai_response
    })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)