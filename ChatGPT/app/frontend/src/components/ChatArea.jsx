import React, { useState } from "react";
import { FaRegUserCircle } from "react-icons/fa";
import { AiFillAliwangwang } from "react-icons/ai";
import axios from "axios";

const PromptBox = ({ onSendMessage, setMsg }) => {
  const [message, setMessage] = useState([]);
  const handleSubmit = (e) => {
    e.preventDefault();
    setMsg((prevMessages) =>
      prevMessages.map((item) => {
        if (
          item.isEditable !== "done" ||
          item.isEditable == false ||
          item.isEditable == true
        ) {
          return { ...item, isEditable: "cancelled" };
        }
        return item;
      })
    );

    if (message && message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <form>
      <label htmlFor="chat" className="sr-only">
        Your message
      </label>
      <div className="flex items-center px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700">
        <button
          type="button"
          className="inline-flex justify-center p-2 text-gray-500 rounded-lg cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600"
        >
          <svg
            className="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 18"
          >
            <path
              fill="currentColor"
              d="M13 5.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0ZM7.565 7.423 4.5 14h11.518l-2.516-3.71L11 13 7.565 7.423Z"
            />
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M18 1H2a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1Z"
            />
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 5.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0ZM7.565 7.423 4.5 14h11.518l-2.516-3.71L11 13 7.565 7.423Z"
            />
          </svg>
          <span className="sr-only">Upload image</span>
        </button>
        <button
          type="button"
          className="p-2 text-gray-500 rounded-lg cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600"
        >
          <svg
            className="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 20"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13.408 7.5h.01m-6.876 0h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM4.6 11a5.5 5.5 0 0 0 10.81 0H4.6Z"
            />
          </svg>
          <span className="sr-only">Add emoji</span>
        </button>
        <textarea
          id="chat"
          rows="1"
          className="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
             
              handleSubmit(e); // Calls the handleSubmit function
            }
          }}
        ></textarea>

        <button
          type="submit"
          onClick={handleSubmit}
          className="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600"
        >
          <svg
            className="w-5 h-5 rotate-90 rtl:-rotate-90"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 18 20"
          >
            <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
          </svg>
          <span className="sr-only">Send message</span>
        </button>
      </div>
    </form>
  );
};

const ChatBubbleLeft = ({ msg, data, setMessages, query, setQuery }) => {
  const handleEditClick = () => {
    setMessages((prevMessages) =>
      prevMessages.map((item) => {
        if (item.id === data.id) {
          return { ...item, isEditable: true };
        }
        return item;
      })
    );
  };

  const handleCancelClick = () => {
    setMessages((prevMessages) =>
      prevMessages.map((item) => {
        if (item.id === data.id) {
          return { ...item, isEditable: "cancelled" };
        }

        return item;
      })
    );
  };

  const handleContinueButton = () => {
    console.log(msg);

    setMessages((prevMessages) =>
      prevMessages.map((item) => {
        if (item.id === data.id) {
          return { ...item, isEditable: "done" };
        }
        if (
          item.isEditable !== "done" ||
          item.isEditable == false ||
          item.isEditable == true
        ) {
          return { ...item, isEditable: "cancelled" };
        }
        return item;
      })
    );
  };

  return (
    <div className="flex items-start gap-2.5 mt-5 box-border">
      <AiFillAliwangwang className="w-8 h-8 rounded-full" />
      <div className="flex flex-col gap-1 w-full max-w-[320px]">
        <div className="flex items-center space-x-2 rtl:space-x-reverse">
          <span className="text-sm font-semibold text-gray-900 dark:text-white">
            RnD
          </span>
        </div>
        <div className="flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700">
          <p
            className="text-sm font-normal text-gray-900 dark:text-white"
            style={{
              display:
                data.isEditable === false ||
                data.isEditable == "done" ||
                data.isEditable == "cancelled"
                  ? "block"
                  : "none",
            }}
          >
            {msg}
          </p>
          <textarea
            className="text-sm font-normal text-gray-900 dark:text-white"
            style={{
              display:
                data.isEditable == "done" ||
                data.isEditable == "cancelled" ||
                data.isEditable == false
                  ? "none"
                  : "block",
            }}
            value={data.reply}
            onChange={(e) => {
              setMessages((prevMessages) =>
                prevMessages.map((msg) => {
                  if (msg.id === data.id) {
                    return { ...msg, reply: e.target.value };
                  }
                  return msg;
                })
              );
            }}
          ></textarea>
        </div>
        <div className="flex">
          {data.isEditable !== "done" && data.isEditable !== "cancelled" && (
            <span
              onClick={handleContinueButton}
              className="cursor-pointer bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300"
            >
              Continue
            </span>
          )}

          {data.isEditable === false && data.isEditable !== "done" && (
            <span
              className="cursor-pointer bg-yellow-100 text-yellow-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full dark:bg-yellow-900 dark:text-yellow-300"
              onClick={handleEditClick}
            >
              Edit
            </span>
          )}

          {data.isEditable !== "done" && data.isEditable !== "cancelled" && (
            <span
              onClick={handleCancelClick}
              className="cursor-pointer bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full dark:bg-red-900 dark:text-red-300"
            >
              Cancel
            </span>
          )}

          {data.isEditable === "cancelled" && (
            <span className="cursor-default bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full dark:bg-red-900 dark:text-red-300">
              Cancelled
            </span>
          )}

          {data.isEditable == "done" && (
            <span className="cursor-default bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300">
              Completed
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

const ChatBubbleRight = ({ message }) => {
  return (
    <div className="flex items-start justify-end gap-2.5 mt-5">
      <div className="flex flex-col gap-1 w-full max-w-[320px]">
        <div className="flex items-center justify-end space-x-2 rtl:space-x-reverse"></div>
        <div className="flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700">
          <p className="text-sm font-normal text-gray-900 dark:text-white">
            {message}
          </p>
        </div>
      </div>
      <FaRegUserCircle className="w-8 h-8 rounded-full" />
    </div>
  );
};

const ChatArea = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");

  const handleSendMessage = (message) => {
    const newMessage = { id: Date.now(), message, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    getResponse(message, newMessage.id);
  };

  const getResponse = async (message, messageId) => {
    try {
      // const response = await axios.post(
      //   "http://127.0.0.1:5000/api/chat",
      //   { query: message },
      //   { headers: { "Content-Type": "application/json" } }
      // );
      const response = {
        data: "This is demo data",
      };
      const reply = response.data;
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: messageId + "_response",
          reply,
          isAltered: false,
          sender: "rnd",
          isEditable: false,
        },
      ]);
    } catch (error) {
      const reply = "Sorry, please try again later!";
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: messageId + "_error", reply, sender: "rnd", isEditable: false },
      ]);
    }
  };

  return (
    <>
      <div className="h-screen flex w-screen box-border">
        <div className="left w-1/5 mr-20 border-black h-dvh"></div>
        <div className="right flex flex-col w-4/5 box-border">
          <div
            className="box-border p-5 w-full"
            style={{
              alignContent: "center",
              overflow: "scroll",
              height: "95vh",
            }}
          >
            {messages.map((msg, index) =>
              msg.sender === "user" ? (
                <ChatBubbleRight key={msg.id} message={msg.message} />
              ) : (
                <ChatBubbleLeft
                  key={msg.id}
                  data={msg}
                  msg={msg.reply}
                  query={query}
                  setQuery={setQuery}
                  setMessages={setMessages}
                />
              )
            )}
          </div>

          <div
            className="fixed bottom-0 right-5 self-center overflow-auto"
            style={{ width: "74%", alignContent: "center" }}
          >
            <PromptBox onSendMessage={handleSendMessage} setMsg={setMessages} />
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatArea;
