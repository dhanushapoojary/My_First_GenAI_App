import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
import time
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Multimodal Q&A App",
    page_icon="🤖",
    layout="wide"
)

# Configure Gemini API
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in environment variables. Please check your .env file.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

# Initialize the model
try:
    model = configure_gemini()
except Exception as e:
    st.error(f"❌ Failed to configure Gemini API: {str(e)}")
    st.stop()

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "current_image_base64" not in st.session_state:
    st.session_state.current_image_base64 = None

# Helper function to convert image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Helper function to process image
def process_uploaded_image(uploaded_file):
    try:
        # Check file size (limit to 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("❌ File size too large. Please upload an image smaller than 10MB.")
            return None
        
        # Open and process image
        image = Image.open(uploaded_file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        return None



# Main app interface
st.markdown("<h1 style='text-align: center;'>🤖 Multimodal Q&A Application</h1>", unsafe_allow_html=True)
st.markdown("Upload an image and ask questions about it using AI!")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Collapsible settings section
    with st.expander("🔧 Model Settings", expanded=False):
        # Temperature control
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, 
                               help="Controls randomness in responses. Lower = more focused, Higher = more creative")
        
        # Top-k control
        top_k = st.slider("Top-K", 1, 40, 20, 1,
                         help="Number of top tokens to consider for generation")
    
    # System prompt display
    with st.expander("📝 System Prompt", expanded=False):
        system_prompt = """You are a helpful AI assistant that can analyze images and answer questions about them. 
        Be descriptive, accurate, and helpful in your responses. If you can't see something clearly in the image, 
        please say so rather than guessing."""
        st.text_area("Current System Prompt", system_prompt, height=100, disabled=True, key="system_prompt_display")
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.current_image = None
        st.session_state.current_image_base64 = None
        st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
        help="Upload an image to ask questions about"
    )
    
    if uploaded_file is not None:
        # Process the uploaded image
        image = process_uploaded_image(uploaded_file)
        
        if image is not None:
            # Store current image in session state
            st.session_state.current_image = image
            st.session_state.current_image_base64 = image_to_base64(image)
            
            # Display the image
            st.image(image, caption="Uploaded Image", width='stretch')
            
            # Show image info
            st.info(f"📊 Image Info: {image.size[0]}x{image.size[1]} pixels, {uploaded_file.size/1024:.1f} KB")
        else:
            st.session_state.current_image = None
            st.session_state.current_image_base64 = None

with col2:
    st.subheader("💬 Ask Questions")
    
    # Text input for questions
    user_question = st.text_input(
        "Enter your question about the image:",
        placeholder="What do you see in this image?",
        key="question_input"
    )
    
    # Ask button - only enabled when there's text
    ask_button = st.button("🤔 Ask", type="primary", disabled=not user_question.strip())
    
    if ask_button and user_question.strip():
        with st.spinner("🤖 AI is thinking..."):
            start_time = time.time()
            
            try:
                # Check if image is available
                if not st.session_state.current_image:
                    st.warning("⚠️ No image uploaded. Please upload an image to ask questions about it.")
                    st.stop()
                
                # Configure generation parameters
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    top_k=top_k,
                    max_output_tokens=1024,
                )
                
                # Create the prompt
                full_prompt = f"{system_prompt}\n\nUser Question: {user_question.strip()}"
                
                # Generate response
                response = model.generate_content(
                    [full_prompt, st.session_state.current_image],
                    generation_config=generation_config
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                # Get the response text
                if response.text:
                    ai_response = response.text
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        "question": user_question.strip(),
                        "answer": ai_response,
                        "response_time": response_time,
                        "timestamp": time.strftime("%H:%M:%S")
                    })
                    
                    # Display the response
                    st.success("✅ Response generated successfully!")
                    st.markdown(f"**AI Response:**")
                    st.markdown(ai_response)
                    
                    # Show response time
                    st.caption(f"⏱️ Response time: {response_time:.2f} seconds")
                    
                else:
                    st.error("❌ No response generated. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.caption("This might be due to API limits, network issues, or content policy violations.")

# Conversation History
if st.session_state.conversation_history:
    st.subheader("📚 Conversation History")
    
    for i, entry in enumerate(reversed(st.session_state.conversation_history)):
        with st.expander(f"Q&A #{len(st.session_state.conversation_history) - i} - {entry['timestamp']}"):
            st.markdown(f"**Question:** {entry['question']}")
            st.markdown(f"**Answer:** {entry['answer']}")
            st.caption(f"Response time: {entry['response_time']:.2f}s")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google Gemini AI")

# Instructions
if not st.session_state.current_image:
    st.info("👆 Please upload an image to get started!")
elif not st.session_state.conversation_history:
    st.info("💡 Ask a question about the uploaded image to begin the conversation!")


