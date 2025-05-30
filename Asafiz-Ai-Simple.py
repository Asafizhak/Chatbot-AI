from flask import Flask, request, jsonify, render_template_string
import boto3
import json
import os

app = Flask(__name__)

# Get configuration from environment variables (GitHub Actions secrets)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
MODEL_ID = os.getenv('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 
    "אתה AI בשם AzureBot, עוזר AI מועיל, מודרני וידידותי. "
    "התייחס לעצמך AzureBot בעת הצורך."
    "אתה מומחה תוכן בעולמות DevOps Azure ספק תמיד תשובות ברורות, תמציתיות ומדויקות."
)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ASAFiz AI | Intelligent Conversations</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #000;
            --foreground: #fff;
            --accent: #1e90ff;
            --bot-msg-bg: #0a1a2a;
            --user-msg-bg: #2a1a0a;
            --border: #222;
        }
        html, body {
            height: 100%;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--background);
            color: var(--foreground);
            min-height: 100vh;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            justify-content: flex-start;
        }
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            width: 100vw;
            position: relative;
        }
        .centerpiece {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 48px;
            margin-bottom: 24px;
        }
        .big-robot {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
        }
        .big-robot img {
            width: 300;
            height: 300px;
            max-width: 95vw;
            max-height: 60vh;
            object-fit: contain;
            display: block;
            margin: 0 auto;
            border-radius: 24px;
            background: #000;
        }
        .main-headline {
            font-size: 3rem;
            font-weight: 900;
            text-align: center;
            letter-spacing: -2px;
            color: #fff;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #fff 60%, #1e90ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header-tagline {
            font-size: 1.15rem;
            color: #bbb;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .chat-container {
            flex: 1;
            width: 100%;
            max-width: 700px;
            padding: 1.5rem 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .message {
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            max-width: 80%;
            font-size: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.3);
            position: relative;
            line-height: 1.6;
            word-break: break-word;
        }
        .user {
            background-color: var(--user-msg-bg);
            margin-left: auto;
            border-bottom-right-radius: 4px;
            color: var(--foreground);
            border: 1px solid #ff9500aa;
        }
        .bot {
            background-color: var(--bot-msg-bg);
            margin-right: auto;
            border-bottom-left-radius: 4px;
            border-left: 3px solid var(--accent);
            border: 1px solid #1e90ff33;
        }
        .input-container {
            width: 100%;
            max-width: 700px;
            padding: 1.5rem 2rem;
            border-top: 1px solid var(--border);
            display: flex;
            background-color: #000;
        }
        #user-input {
            flex-grow: 1;
            padding: 1rem 1.2rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-right: 1rem;
            font-size: 1rem;
            background-color: #111;
            color: #fff;
        }
        button {
            padding: 0 1.5rem;
            background: linear-gradient(135deg, #1e90ff, #222);
            color: #fff;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        button svg {
            margin-left: 6px;
        }
        button:hover {
            box-shadow: 0 0 15px #1e90ff44;
            transform: translateY(-1px);
        }
        .thinking-indicator {
            display: none;
            background-color: var(--bot-msg-bg);
            margin-right: auto;
            border-bottom-left-radius: 4px;
            border-left: 3px solid var(--accent);
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            max-width: 80%;
            font-size: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.3);
            position: relative;
        }
        .thinking-indicator.active {
            display: flex;
            align-items: center;
        }
        .thinking-dots {
            display: flex;
        }
        .thinking-dots span {
            width: 8px;
            height: 8px;
            margin: 0 2px;
            background-color: var(--accent);
            border-radius: 50%;
            animation: dot-pulse 1.5s infinite;
        }
        .thinking-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .thinking-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes dot-pulse {
            0%, 100% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.2); opacity: 1; }
        }
        /* RTL support for Hebrew text */
        .message.rtl {
            direction: rtl;
            text-align: right;
        }
        .bot.rtl {
            margin-left: auto;
            margin-right: 0;
            border-left: none;
            border-right: 3px solid var(--accent);
            border-bottom-right-radius: 4px;
            border-bottom-left-radius: 12px;
            border: 1px solid #1e90ff33;
        }
        @media (max-width: 900px) {
            .big-robot img {
                width: 300px;
                height: 300px;
            }
        }
        @media (max-width: 600px) {
            .big-robot img {
                width: 160px;
                height: 160px;
            }
            .main-headline {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="main-content">
        <div class="centerpiece">
            <div class="big-robot">
                <img src="https://i.pinimg.com/originals/0b/1b/ff/0b1bff36918c2e231d1a980b2c4c3cef.gif" alt="AI Robot" />
            </div>
            <h1 class="main-headline">ASAFiz AI</h1>
            <div class="header-tagline">Intelligent conversations powered by AWS Bedrock</div>
        </div>
        <div class="chat-container" id="chat-container"></div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message here...">
            <button onclick="sendMessage()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m22 2-7 20-4-9-9-4Z"></path>
                    <path d="M22 2 11 13"></path>
                </svg>
            </button>
        </div>
    </div>
    <script>
        let messages = [];
        let isProcessing = false;
        function addMessage(content, isUser) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            // Detect Hebrew text (Unicode range for Hebrew characters)
            const hebrewRegex = /[\u0590-\u05FF]/;
            const isHebrew = hebrewRegex.test(content);
            
            if (isHebrew && !isUser) {
                messageDiv.classList.add('rtl');
            }
            
            messageDiv.innerText = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            messages.push({
                role: isUser ? 'user' : 'assistant',
                content: content
            });
        }
        function showThinking() {
            isProcessing = true;
            const chatContainer = document.getElementById('chat-container');
            const thinkingDiv = document.createElement('div');
            thinkingDiv.className = 'thinking-indicator active';
            thinkingDiv.id = 'thinking-indicator';
            const thinkingIcon = document.createElement('div');
            thinkingIcon.className = 'thinking-icon';
            const dotsDiv = document.createElement('div');
            dotsDiv.className = 'thinking-dots';
            for (let i = 0; i < 3; i++) {
                const dot = document.createElement('span');
                dotsDiv.appendChild(dot);
            }
            thinkingDiv.appendChild(thinkingIcon);
            thinkingDiv.appendChild(dotsDiv);
            chatContainer.appendChild(thinkingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        function hideThinking() {
            isProcessing = false;
            const thinkingDiv = document.getElementById('thinking-indicator');
            if (thinkingDiv) {
                thinkingDiv.remove();
            }
        }
        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const userMessage = userInput.value.trim();
            if (userMessage) {
                addMessage(userMessage, true);
                userInput.value = '';
                showThinking();
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        messages: messages
                    })
                })
                .then(response => response.json())
                .then(data => {
                    hideThinking();
                    addMessage(data.response, false);
                })
                .catch(error => {
                    hideThinking();
                    console.error('Error:', error);
                    addMessage('Error: Could not get response from the server.', false);
                });
            }
        }
        document.getElementById('user-input').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

def call_bedrock_llm(messages):
    """Call AWS Bedrock LLM with the provided credentials and messages."""
    try:
        # Check if required environment variables are set
        if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
            return "Error: AWS credentials not configured. Please set AWS_ACCESS_KEY and AWS_SECRET_KEY environment variables."
        
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        
        # Remove any 'system' role messages from the frontend (should never be present)
        filtered_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages if m["role"] in ("user", "assistant")
        ]
        
        # Format content as string or list as needed
        for m in filtered_messages:
            if isinstance(m["content"], str):
                m["content"] = [{"type": "text", "text": m["content"]}]
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.7,
            "system": SYSTEM_PROMPT,
            "messages": filtered_messages
        }
        
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]
        
    except Exception as e:
        return f"Error calling Bedrock LLM: {str(e)}"

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    response_text = call_bedrock_llm(messages)
    return jsonify({
        'response': response_text
    })

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'aws_configured': bool(AWS_ACCESS_KEY and AWS_SECRET_KEY),
        'region': AWS_REGION,
        'model': MODEL_ID
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')