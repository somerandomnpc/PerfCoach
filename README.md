# Perf Coach

An AI-powered Streamlit app that analyzes YouTube comments by timestamp and offers text + voice coaching feedback.

## 🛠️ Setup & Deployment (Streamlit Cloud)

1. Fork or clone this repo.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and create a new app, linking to this repository.
3. In **Settings > Secrets**, add:
   - `GOOGLE_API_KEY`
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY` (optional)
4. Deploy – you’ll get a public URL!
5. Paste in a YouTube video link to get instant feedback.

## 🔧 Local Testing

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
