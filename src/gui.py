import streamlit as st
import requests
import json

# --- 1. Oturum Durumunu Başlatma ---
# Bu, verilerin (özet ve mesajlar) sayfa yenilense bile korunmasını sağlar.
if "summary" not in st.session_state:
    st.session_state.summary = None
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("YT Q&A Assistant")
url_input = st.text_input("Enter video url")


button = st.button("↵")

if button:
    if url_input:
        res_transcript = requests.post(url="http://127.0.0.1:8000/add_transcript_to_system", params={"video_url": url_input})
        print(res_transcript.text)

        if res_transcript.status_code == 200:
            res_summary = requests.post(url="http://127.0.0.1:8000/summarize", params={"transcript": res_transcript})
            print(res_summary.text)

            if res_summary.status_code == 200:
                st.session_state.summary = res_summary.text # Özeti Session State'e kaydet
                st.session_state.messages = [] # Yeni özet geldiğinde eski sohbeti temizle
                st.success("Özet başarıyla alındı!")


            



# --- 3. Özet Görüntüleme ve Q&A Aşaması ---

# Eğer özet oturum durumunda mevcutsa (yani başarıyla alınmışsa) göster
if st.session_state.summary:
    st.subheader("Video Özeti")

    summary = json.loads(st.session_state.summary)
    st.write(summary.get("video_title"))
    st.write("\n")
    st.write(summary.get("summary"))
    st.write("\n")
    st.write("Anahtar Çıkarımlar")
    st.write(summary.get("key_takeaways"))

    st.markdown("---")
    st.subheader("Soru-Cevap (Q&A) Başlatın")

    # Geçmiş mesajları görüntüle
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Yeni kullanıcı girdisi alımı için modern arayüz
    if user_question := st.chat_input("Özet hakkında bir soru sorun..."):
        
        # 3a. Kullanıcı mesajını geçmişe ekle ve göster
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        # 3b. Chat API'sine Gönderme
        try:
            with st.spinner("Yanıt aranıyor..."):
                res_chat = requests.post(
                    url="http://127.0.0.1:8000/chat", 
                    params={"question": user_question}
                )
                
                if res_chat.status_code == 200:
                    bot_response = res_chat.text
                else:
                    bot_response = f"API'den yanıt alınamadı. Durum Kodu: {res_chat.status_code}"

        except requests.exceptions.ConnectionError:
            bot_response = "API sunucusuna bağlanılamadı. Lütfen sunucunun çalıştığından emin olun."
        except Exception as e:
            bot_response = f"Bir hata oluştu: {e}"

        # 3c. Bot mesajını geçmişe ekle ve göster
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

