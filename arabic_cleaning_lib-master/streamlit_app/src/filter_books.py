import json
import os

import streamlit as st


@st.cache_resource
def load_data(data_path):
    data = []
    if data_path is None:
        return data
    with open(data_path, "r") as f:
        for line in f:
            doc = json.loads(line)
            if "chosen" not in doc:
                doc["chosen"] = 0
            data.append(doc)
    return data


def save_data(data, data_path):
    with open(f"{data_path}_temp", "w") as f_w:
        for doc in data:
            f_w.write(json.dumps(doc, ensure_ascii=False))
            f_w.write("\n")
    with open(data_path, "w") as f_w:
        for doc in data:
            f_w.write(json.dumps(doc, ensure_ascii=False))
            f_w.write("\n")


def main():
    st.title("Books relavent to Public finance")

    st.sidebar.title("Almanhal")
    options = sorted(
        [
            op[op.find("batch") : op.rfind(".jsonl")]
            for op in os.listdir("/data/almanhal/")
            if op.rfind("_temp") < 0
        ]
    )
    dataset_name = st.sidebar.selectbox(
        "Choose a batch",
        options=options,
        index=None,
    )
    data_path = (
        f"/data/almanhal/almanahl_first_pages_{dataset_name}.jsonl"
        if dataset_name is not None
        else None
    )
    data = load_data(data_path)
    if "page_number" not in st.session_state:
        st.session_state["page_number"] = 1
    cols = st.columns(6)
    with cols[0]:
        left_clicked = st.button("<")
        if left_clicked and st.session_state["page_number"] > 1:
            st.session_state["page_number"] -= 1
    with cols[2]:
        clicked = st.button(r"\>")
        if clicked and st.session_state["page_number"] < len(data):
            st.session_state["page_number"] += 1
    with cols[3]:
        unseen_clicked = st.button(r"Next Unseen")
        if unseen_clicked:
            for i in range(len(data)):
                if data[i]["chosen"] == 0:
                    st.session_state["page_number"] = i + 1
                    break
            else:
                st.session_state["page_number"] = len(data)

    # with cols[4]:
    #     remove_clicked = st.button("Unrelavent")
    #     if remove_clicked:
    #         data[st.session_state["page_number"] - 1]["chosen"] = -1
    #         st.session_state["page_number"] += 1
    #         save_data(data, data_path)
    with cols[5]:
        if len(data):
            label = None
            if data[st.session_state["page_number"] - 1]["chosen"] == 1:
                label = "Unrelavent"
            else:
                label = "Relavent"
            add_clicked = st.button(label)
            if add_clicked:
                if data[st.session_state["page_number"] - 1]["chosen"] == 0:
                    data[st.session_state["page_number"] - 1]["chosen"] = 1
                else:
                    data[st.session_state["page_number"] - 1]["chosen"] = (
                        0 - data[st.session_state["page_number"] - 1]["chosen"]
                    )
                st.session_state["page_number"] += 1
                save_data(data, data_path)

    with cols[4]:
        if len(data):
            with st.container(border=True):
                # st.text([i["chosen"] for i in data[:10]])
                if data[st.session_state["page_number"] - 1]["chosen"] == 1:
                    st.text("\u2714")
                elif data[st.session_state["page_number"] - 1]["chosen"] == -1:
                    st.text("\u2718")
                else:
                    st.text("Unseen")
    with cols[1]:
        st.session_state["page_number"] = int(
            st.text_input(
                f"Total: {len(data) if len(data) else 0}",
                value=st.session_state["page_number"],
            )
        )
    with st.container(border=True):
        if len(data):
            st.text(data[st.session_state["page_number"] - 1]["text"])

        else:
            st.markdown("Please choose a dataset from the left menu")


if __name__ == "__main__":
    main()
