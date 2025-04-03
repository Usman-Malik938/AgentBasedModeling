from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient  # Correct import

app = Flask(__name__)


information = """
# Helpfull information and statistics

- 91% of remote teams report improved collaboration with scheduled weekly progress updates (Gartner, 2019). Example: Use tools like Standuply or 
  Microsoft Teams for automated check-ins.

- 61% of teams achieve higher productivity when tasks are well-defined and prioritized (Harvard Business Review, 2019). Example: Implement OKRs using 
  Trello or Asana to track goals.

- 76% of remote workers favor a single channel for project updates, improving task coordination (Stanford University, 2018). Example: Use Slack or 
  Microsoft Teams for streamlined communication.

"""

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
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400


    prompt_template = ChatPromptTemplate.from_template(
        """
        I need to experiment with a question on multiple users, where each user will provide ideas on the given question. You have to generate a very minor variation in the given information to be provided to every user. The variation should be very minimal to avoid bias for every user.

        Return only the final adjusted response, with no additional text or commentary. The generated response should vary slightly each time it's called, ensuring medium changes that do not alter the core meaning or intent of the information. The response must not include headings or subheadings. Do not use phrases that could be interpreted as headings, such as "Improved Collaboration" or "Higher Productivity." Instead, present each point directly in a bullet point format.

        Every key point must be presented in the format: 
        - [Statistic] ([Source, Year]). Example: [Example of how to apply the statistic]

        Ensure that every piece of information is factual, supported by concrete data, and properly sourced. Keep different sections clearly separated to enhance readability. Do not include introductions, conclusions, or irrelevant content.

        Question: {question}

        Information: {information}

        Response:
        """
    )



#        - There can be slight increase and decrease in number of bullet points in each call



    prompt = prompt_template.format(question=question, information=information)

    try:
        response = llm1.invoke(prompt)
        ai_response = response.content.strip()
    except Exception as e:
        return jsonify({"error": f"AI Response Failed: {str(e)}"}), 500

    # === Step 2: Fetch References from Tavily ===
    try:
        tavily_response = tavily.search(query=question, num_results=3)  # API call
        print("#################################################3Tavily Response:", tavily_response)  # Debugging line

        references = [
            {"title": result.get("title", "No Title"), "url": result.get("url", "No URL")}
            for result in tavily_response.get("results", [])[:3]
        ]

    except Exception as e:
        references = [{"error": f"Failed to fetch references: {str(e)}"}]

    # === Step 3: Evaluate AI Response ===
    eval_prompt_template = ChatPromptTemplate.from_template(
        """
        ### **Question:** {question}

        ### **Information:** {information}

        ### **Agent 1's Response:**
        {response1}

        ### **Agent 2 Instructions:**
        - **DO NOT** include any ending notes for **changes** you will made , explanations, or change notes.
        - Review Agent 1's response and adjust it for accuracy while ensuring minimal variation from the original information.
        - Focus on **preserving the meaning and clarity** of the original content.
        - **Return only the final adjusted response**, with no additional text or commentary.
        
        ## **Forced to notice**
        - There should be no starting and ending notes for the **minor changes** or **minor variations** you have made
        ### **Final Adjusted Response:**
        {updated_response}
        """
    )




    #evaluation = "hello############################"
    eval_prompt = eval_prompt_template.format(
        question=question,
        information=information,
        response1=ai_response,
        updated_response=ai_response  # This remains the same
    )


    try:
        eval_response = llm2.invoke(eval_prompt)
        evaluation = eval_response.content.strip()
    except Exception as e:
        evaluation = f"Evaluation failed: {str(e)}"

    # === Step 4: Return JSON Response ===
    return jsonify({
        "response": ai_response,
        "evaluation": evaluation,
        "references": references
    })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
