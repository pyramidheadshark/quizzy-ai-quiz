import streamlit as st
import pandas as pd
import os
from modules.quiz_manager import QuizManager
from modules.quiz_generator import QuizGenerator
from modules.data_storage import JsonDataStorage
from modules.statistics import Statistics

st.set_page_config(page_title="Quiz Generator", layout="wide")

storage = JsonDataStorage()
generator = QuizGenerator()
manager = QuizManager(storage, generator)
stats = Statistics()

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a page", ["Home", "Create Quiz", "Quiz Library", "Statistics"],
                    label_visibility="collapsed")

st.title("Quiz Generator")

if page == "Home":
    st.subheader("Welcome!")
    st.write("Create and take quizzes for learning or fun.")

elif page == "Create Quiz":
    st.subheader("Create a new quiz")
    with st.form("create_quiz_form"):
        title = st.text_input("Quiz Title", help="Enter a unique title for your quiz")
        theme = st.text_input("Quiz Theme", help="Specify a theme, for example, 'History', 'Science'")
        language = st.text_input("Question Language", value="Russian", help="For example, 'Russian', 'English'")
        difficulty = st.text_input("Difficulty", value="medium", help="Difficulty level: easy, medium, hard")
        num_questions_input = st.text_input("Number of questions", value="5", help="Enter a number or a word, for example, '5' or 'five'")
        material_type = st.selectbox("Material Type", ["Text", "File"], help="Choose how to provide the material")
        material = ""
        if material_type == "Text":
            material = st.text_area("Enter text", height=200, help="Enter text for question generation")
        elif material_type == "File":
            uploaded_file = st.file_uploader("Upload file", type=["txt"], help="Upload a text file")
            if uploaded_file:
                material = uploaded_file.read().decode("utf-8")
        submit_button = st.form_submit_button("Generate Quiz")

    if submit_button:
        if all([title, theme, language, difficulty, material]):
            try:
                num_questions_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
                num_questions = num_questions_dict.get(num_questions_input.lower(), int(num_questions_input or 5))
                quiz = manager.create_quiz(title, theme, material, language, difficulty, num_questions)
                st.success(f"Quiz '{quiz.title}' created! ID: {quiz.id}")
            except ValueError:
                st.error("Please enter a valid number of questions (digit or word)")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in all fields.")

elif page == "Quiz Library":
    st.subheader("Quiz Library")
    quiz_titles = manager.list_quiz_titles()
    if quiz_titles:
        selected_title = st.selectbox("Select a quiz", list(quiz_titles.values()))
        selected_quiz_id = [k for k, v in quiz_titles.items() if v == selected_title][0]
        quiz = manager.get_quiz(selected_quiz_id)
        st.write(f"Theme: {quiz.theme}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Take Quiz"):
                st.session_state["current_quiz"] = quiz
                st.session_state["answers"] = {}
                st.session_state["current_question"] = 0
                st.session_state["quiz_started"] = True
        with col2:
            new_title = st.text_input("New title", value=quiz.title)
            if st.button("Rename") and new_title != quiz.title:
                manager.rename_quiz(selected_quiz_id, new_title)
                st.success(f"Quiz renamed to '{new_title}'")
                st.rerun()
        with col3:
            if st.button("Delete Quiz"):
                st.session_state["delete_quiz_id"] = selected_quiz_id
                st.session_state["show_delete_confirmation"] = True

        if st.session_state.get("show_delete_confirmation", False):
            st.write("Are you sure you want to delete this quiz?")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("Confirm"):
                    manager.delete_quiz(st.session_state["delete_quiz_id"])
                    st.success("Quiz deleted")
                    st.session_state["show_delete_confirmation"] = False
                    st.rerun()
            with col_cancel:
                if st.button("Cancel"):
                    st.session_state["show_delete_confirmation"] = False
                    st.rerun()

        if st.session_state.get("quiz_started", False) and st.session_state.get("current_quiz") == quiz:
            total_questions = len(quiz.questions)
            current_idx = st.session_state["current_question"]

            st.write(f"Question {current_idx + 1} of {total_questions}")
            st.progress((current_idx + 1) / total_questions)

            q = quiz.questions[current_idx]
            st.write(f"Question {current_idx + 1}: {q['question']}")
            saved_answer = st.session_state["answers"].get(current_idx)
            default_index = q["options"].index(saved_answer) if saved_answer in q["options"] else 0
            answer = st.radio("Choose an answer", q["options"], key=f"q{current_idx}", index=default_index)
            st.session_state["answers"][current_idx] = answer

            col_prev, col_next, col_finish = st.columns(3)
            with col_prev:
                if st.button("Previous", disabled=current_idx == 0):
                    st.session_state["current_question"] -= 1
                    st.rerun()
            with col_next:
                if st.button("Next", disabled=current_idx == total_questions - 1):
                    st.session_state["current_question"] += 1
                    st.rerun()
            with col_finish:
                if st.button("Finish Quiz"):
                    correct_count = 0
                    results = []
                    for i, q in enumerate(quiz.questions):
                        user_answer = st.session_state["answers"].get(i)
                        correct_option = q["options"][ord(q["correct_answer"]) - ord("A")]
                        is_correct = user_answer == correct_option
                        if is_correct:
                            correct_count += 1
                        results.append({
                            "question": q["question"],
                            "user_answer": user_answer if user_answer else "Not selected",
                            "correct_answer": correct_option,
                            "is_correct": is_correct
                        })

                    total = total_questions
                    percentage = (correct_count / total) * 100 if total > 0 else 0
                    st.write(f"Result: {correct_count}/{total} ({percentage:.2f}%)")

                    for i, result in enumerate(results):
                        with st.expander(f"Question {i + 1}: {'Correct' if result['is_correct'] else 'Incorrect'}"):
                            st.write(f"Question: {result['question']}")
                            st.write(f"Your answer: {result['user_answer']}")
                            st.write(f"Correct answer: {result['correct_answer']}")

                    stats.add_record(quiz.id, correct_count, total)
                    st.session_state["quiz_started"] = False
    else:
        st.info("No quizzes in the library.")

elif page == "Statistics":
    st.subheader("Statistics")
    df = stats.get_statistics()
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        st.write(f"Total quizzes: {len(df)}")
        st.write(f"Average percentage: {df['percentage'].mean():.2f}%")
        st.line_chart(df.set_index("timestamp")["percentage"])
    else:
        st.info("No statistics data available.")