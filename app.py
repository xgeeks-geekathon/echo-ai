
import gradio as gr
import openai
import dotenv
import os

import topics
import youtube_video_utils
import process_utils
import quiz

import top_words
import keywords


dotenv.load_dotenv()

openai.api_key=os.environ["OPENAI_API_KEY"]

def handle_translate_button(file):
    return process_utils.process_file(file, True)

def handle_transcribe_button(file):
    return process_utils.process_file(file, False)

def get_topics(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8-sig') as f:
        data, merged_data = topics.createTopics(f.read())
        return (data, gr.Dropdown.update(choices=merged_data,interactive=True))

def get_keywords(resume, transcribed_text):
    return keywords.createDefinitions(transcribed_text, resume)

def count_words(text):
    return top_words.findTopWords(text)

def get_quiz(transcribed_text, num_open_question, multiple_option_question):
    return quiz.createQuestions(transcribed_text, num_open_question, multiple_option_question)

def get_youtube_video(url):
    file = youtube_video_utils.download_video(url)
    return handle_transcribe_button(file)

def get_youtube_video_translate(url):
    file = youtube_video_utils.download_video(url)
    return handle_translate_button(file)

with gr.Blocks() as demo:
    gr.Markdown("# EchoAI - Upload your audio or video file")

    with gr.Tab(label="Transcribe"): 
        upload_button = gr.UploadButton("Click to Upload an Audio or Video File", file_types=["audio", "video"], file_count="single")
        youtube_url = gr.Textbox(label="Youtube URL")
        youtube_url_button = gr.Button(label="Transcribe from Youtube", variant="secondary")

        display_bar = gr.Video(show_label=False, type="filepath", elem_id="#display", interactive=False)

        with gr.Column(visible=False) as show_outputs:
            gr.Markdown("## Summary")
            resume = gr.Textbox(label="Summary", lines=5)
            
            gr.Markdown("## Transcribed Text")
            transcribed_text = gr.Textbox(label="Transcribed Text", lines=5)

            path_to_file = gr.Textbox(visible=False)
            path_to_file_srt = gr.Textbox(visible=False)

            with gr.Row():
                with gr.Column():
                    gr.Markdown("## Word Counter")
                    word_counter_text = gr.Textbox(label="Word Counter",lines=5)
                    word_counter_btn = gr.Button(value = "Get Word Counter")
                    word_counter_btn.click(count_words, inputs=[transcribed_text], outputs=[word_counter_text])
                with gr.Column():
                    gr.Markdown("## Topics")
                    topics_text = gr.Textbox(label="Topics", lines=5)
                    topics_button = gr.Button(label="Get Topics", variant="secondary")

                    drop = gr.Dropdown(choices=[],label="Timestamps", elem_id="#dropdown")
                    
                    button = gr.Button(value="Jump To",label="Jump To", elem_id="#gotobutton")
                    
                    topics_button.click(get_topics, inputs=[path_to_file_srt], outputs=[topics_text, drop])

            with gr.Row():
                with gr.Column():
                    gr.Markdown("## Keywords")
                    keywords_text = gr.Textbox(label="Keywords", lines=5)
                    keywords_button = gr.Button(label="Get Keywords", variant="secondary")
                    keywords_button.click(get_keywords, inputs=[resume, transcribed_text], outputs=[keywords_text])

            with gr.Row():
                with gr.Column():
                    gr.Markdown("## Quiz")
                    num_open_question = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="Open Question", elem_id="#slider")
                    multiple_option_question = gr.Slider(minimum=0, maximum=10, value=0, step=1, label="Multiple Option Question", elem_id="#slider")
                    quiz_text = gr.Textbox(label="Quiz", lines=5, show_copy_button=True)
                    quiz_button = gr.Button(label="Get Quiz", variant="secondary")
                    quiz_button.click(get_quiz, inputs=[transcribed_text, num_open_question, multiple_option_question], outputs=[quiz_text])

        clear_button = gr.ClearButton(variant="stop", components=[topics_text, keywords_text, resume, transcribed_text, word_counter_text, quiz_text, display_bar, drop, youtube_url])
        clear_button.click(lambda: gr.Row.update(visible=False), outputs=show_outputs)

        upload_button.upload(handle_transcribe_button, inputs=[upload_button], outputs=[resume, transcribed_text, path_to_file, path_to_file_srt, display_bar, show_outputs])
        youtube_url_button.click(get_youtube_video, inputs=[youtube_url], outputs=[resume, transcribed_text, path_to_file, path_to_file_srt, display_bar, show_outputs])

    with gr.Tab(label="Translate"):
        upload_button_translate = gr.UploadButton("Click to Upload an Audio or Video File", file_types=["audio", "video"], file_count="single")
        youtube_url_translate = gr.Textbox(label="Youtube URL")
        youtube_url_button_translate = gr.Button(label="Transcribe from Youtube", variant="secondary")
        
        display_bar_translate = gr.Video(show_label=False, type="filepath", elem_id="#displayTranslate", interactive=False)

        with gr.Row(visible=False) as show_outputs_translate:
            with gr.Column():
                gr.Markdown("## Translation")
                translation = gr.Textbox(label="Translation", lines=5)

        clear_button_translate = gr.ClearButton(variant="stop", components=[translation, display_bar_translate, youtube_url_translate])
        clear_button_translate.click(lambda: gr.Row.update(visible=False), outputs=show_outputs_translate)

        upload_button_translate.upload(handle_translate_button, inputs=[upload_button_translate], outputs=[translation, display_bar_translate, show_outputs_translate])
        youtube_url_button_translate.click(get_youtube_video_translate, inputs=[youtube_url_translate], outputs=[translation, display_bar_translate, show_outputs_translate])

    demo.load(_js="""
        function my_func() {
            let gradioEl = document.querySelector('body > gradio-app:nth-child(1)');
            const button = gradioEl.querySelector('button[id="#gotobutton"]');
              
            button.addEventListener("click", e => {
                const dropdown = gradioEl.querySelector('div[id="#dropdown"] input');
                const timestamp = dropdown.value.split('->')[1];
              
                setTimeout(() => {
                    let videoplayer = gradioEl.querySelector('video[data-testid="test-player"]');
                    videoplayer.currentTime = timestamp;
                })
            })
        }
    """)



if __name__ == "__main__":
    demo.launch()