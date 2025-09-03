# Multimodal Q&A Application

A simple Streamlit application that allows users to upload images and ask questions about them using Google's Gemini 2.5 Flash model.

## Features

### Must-haves ✅
- **File uploader** for images (PNG, JPG, JPEG, GIF, BMP)
- **Text input** for questions about the uploaded image
- **Single "Ask" action** that calls the model and renders the answer
- **Conversation history** for follow-up questions about the same image
- **Graceful error handling** for missing images, oversized files, and API errors

### Nice-to-haves ✨
- **System prompt display** and customization
- **Temperature and max tokens controls** for model behavior tuning
- **Response time display** for performance monitoring
- **Clean, modern UI** with proper layout and styling

## Setup

1. **Clone or download** this repository

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Gemini API key**:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## Usage

1. **Upload an image** using the file uploader in the left column
2. **Enter your question** in the text area in the right column
3. **Click "Ask"** to get an AI response about the image
4. **Ask follow-up questions** - the conversation history is maintained
5. **Adjust model parameters** using the sidebar controls
6. **Clear conversation** anytime using the sidebar button

**Note**: Make sure your virtual environment is activated before running the app. You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

## Error Handling

The application handles various error scenarios:
- **Missing image**: Shows error message when trying to ask without uploading
- **Oversized files**: Validates file size (max 20MB) and shows appropriate error
- **Invalid image formats**: Validates image format and shows error for unsupported files
- **API errors**: Handles rate limits, API errors, and network issues gracefully
- **Missing API key**: Shows clear error message if OpenAI API key is not set

## Technical Details

- **Framework**: Streamlit
- **LLM**: Google Gemini 2.5 Flash (gemini-2.5-flash)
- **Image processing**: PIL (Pillow)
- **Environment management**: python-dotenv
- **Session management**: Streamlit session state for conversation history

## File Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env               # Environment variables (create this)
```

## API Costs

This application uses Google's Gemini 2.5 Flash API, which has associated costs:
- **Input tokens**: ~$0.000075 per 1K tokens
- **Output tokens**: ~$0.0003 per 1K tokens
- **Images**: Included in input token count

Monitor your usage on the [Google AI Studio Dashboard](https://aistudio.google.com/app/apikey).

## Troubleshooting

### Common Issues

1. **"Please set your GEMINI_API_KEY" error**:
   - Make sure you have a `.env` file with your API key
   - Verify the API key is correct and has sufficient credits

2. **"Rate limit exceeded" error**:
   - Wait a moment and try again
   - Consider upgrading your Google AI Studio plan if you hit limits frequently

3. **Image upload issues**:
   - Ensure the image is in a supported format (PNG, JPG, JPEG, GIF, BMP)
   - Check that the file size is under 20MB
   - Try a different image if the current one is corrupted

4. **App won't start**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using Python 3.8 or higher

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## License

This project is open source and available under the MIT License.
