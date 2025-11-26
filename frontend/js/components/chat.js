class ChatComponent {
  constructor(onAddToLog = null) {
    this.chatContainer = document.getElementById('chat-container');
    this.chatMessages = document.getElementById('chat-messages');
    this.chatInput = document.getElementById('chat-input');
    this.chatSendBtn = document.getElementById('chat-send-btn');
    this.chatToggle = document.getElementById('chat-toggle');
    this.chatClose = document.getElementById('chat-close');
    
    this.conversationHistory = [];
    this.isOpen = false;
    this.onAddToLog = onAddToLog; // Callback to add food to the log
    
    this.bindEvents();
    this.addWelcomeMessage();
  }

  bindEvents() {
    this.chatToggle.addEventListener('click', () => this.toggleChat());
    this.chatClose.addEventListener('click', () => this.toggleChat());
    this.chatSendBtn.addEventListener('click', () => this.sendMessage());
    this.chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    this.chatContainer.classList.toggle('open', this.isOpen);
    this.chatToggle.classList.toggle('hidden', this.isOpen);
    if (this.isOpen) {
      this.chatInput.focus();
    }
  }

  addWelcomeMessage() {
    this.addMessage('assistant', "Hi! 👋 I'm your nutrition assistant. Tell me what you're eating and I'll help you track the nutritional info. For example, try saying \"I had a chicken sandwich for lunch\" or \"How many calories are in an avocado?\"");
  }

  addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    // Parse nutrition data from the content
    const { displayContent, nutritionData } = this.parseNutritionData(content);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = this.formatMessage(displayContent);
    
    messageDiv.appendChild(contentDiv);
    
    // Add "Add to Log" button if nutrition data is present and callback exists
    if (nutritionData && this.onAddToLog) {
      const addButton = this.createAddToLogButton(nutritionData);
      messageDiv.appendChild(addButton);
    }
    
    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  parseNutritionData(content) {
    // Look for the nutrition data tag: <!--NUTRITION_DATA:{...}-->
    const regex = /<!--NUTRITION_DATA:(\{[^}]+\})-->/;
    const match = content.match(regex);
    
    let nutritionData = null;
    let displayContent = content;
    
    if (match) {
      try {
        nutritionData = JSON.parse(match[1]);
        // Remove the nutrition data tag from display content
        displayContent = content.replace(regex, '').trim();
      } catch (e) {
        console.error('Failed to parse nutrition data:', e);
      }
    }
    
    return { displayContent, nutritionData };
  }

  createAddToLogButton(nutritionData) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'add-to-log-container';
    
    const button = document.createElement('button');
    button.className = 'add-to-log-btn';
    button.innerHTML = `
      <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
      </svg>
      Add to Log
    `;
    
    button.addEventListener('click', () => {
      if (this.onAddToLog) {
        this.onAddToLog({
          name: nutritionData.name || 'Food Item',
          calories: nutritionData.calories || 0,
          protein: nutritionData.protein || 0,
          carbs: nutritionData.carbs || 0,
          fat: nutritionData.fat || 0
        });
        
        // Show success feedback
        button.classList.add('added');
        button.innerHTML = `
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
          </svg>
          Added!
        `;
        button.disabled = true;
      }
    });
    
    buttonContainer.appendChild(button);
    return buttonContainer;
  }

  formatMessage(content) {
    // Convert line breaks to <br> and basic markdown
    return content
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/- (.*?)(?=<br>|$)/g, '• $1');
  }

  addTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'chat-message assistant typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<div class="message-content"><span></span><span></span><span></span></div>';
    this.chatMessages.appendChild(indicator);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  async sendMessage() {
    const message = this.chatInput.value.trim();
    if (!message) return;

    // Add user message to UI
    this.addMessage('user', message);
    this.chatInput.value = '';
    this.chatInput.disabled = true;
    this.chatSendBtn.disabled = true;

    // Show typing indicator
    this.addTypingIndicator();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          history: this.conversationHistory
        })
      });

      const data = await response.json();
      
      // Remove typing indicator
      this.removeTypingIndicator();

      if (data.status === 'success') {
        // Add to history
        this.conversationHistory.push({ role: 'user', content: message });
        this.conversationHistory.push({ role: 'assistant', content: data.response });
        
        // Keep history manageable (last 10 exchanges)
        if (this.conversationHistory.length > 20) {
          this.conversationHistory = this.conversationHistory.slice(-20);
        }
        
        // Add assistant response to UI
        this.addMessage('assistant', data.response);
      } else {
        this.addMessage('assistant', 'Sorry, I had trouble processing that. Please try again.');
      }
    } catch (error) {
      console.error('Chat error:', error);
      this.removeTypingIndicator();
      this.addMessage('assistant', 'Sorry, I couldn\'t connect to the server. Please try again.');
    }

    this.chatInput.disabled = false;
    this.chatSendBtn.disabled = false;
    this.chatInput.focus();
  }
}

export default ChatComponent;

