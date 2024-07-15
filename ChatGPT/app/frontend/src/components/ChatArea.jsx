import React, { useEffect, useState } from "react";
import { FaRegUserCircle } from "react-icons/fa";
import { AiFillAliwangwang } from "react-icons/ai";
import axios from "axios";
import { API_URL } from "../config";
import { useRef } from "react";
import classNames from "classnames";
import "./ChatAreaCss.scss";
import { CopyBlock } from "react-code-blocks";

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
      <div className="flex items-center px-3 py-2 rounded-lg bg-gray-50 ">
        <button
          type="button"
          className="inline-flex justify-center p-2 text-gray-500 rounded-lg cursor-pointer hover:text-gray-900 hover:bg-gray-100"
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
          className="p-2 text-gray-500 rounded-lg cursor-pointer hover:text-gray-900 hover:bg-gray-100 "
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
          className="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 "
          placeholder="Your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              handleSubmit(e);
            }
          }}
        ></textarea>

        <button
          type="submit"
          onClick={handleSubmit}
          className="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 "
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

  const handleContinueButton = async () => {
    console.log(msg);
    try {
      const response = await axios.post(
        `${API_URL}/api/continue`,
        // `/api/continue`,
        {
          reply: data.reply,
          question: data.question,
          function_name: data.function_name,
          function_args: data.function_args,
          tools: data.tools,
          uid: data.uid,
          tool_calls: data.tool_calls,
          tool_call_id: data.tool_call_id,
        },
        { headers: { "Content-Type": "application/json" } }
      );

      // const finalData = response.data[0]
      console.log(response.data);
      setMessages((prevMessages) =>
        prevMessages.map((item) => {
          if (item.id === data.id) {
            return { ...item, isOutput: response.data[0].answer};
          }
          
        
          return item;
        })
      );
    } catch (error) {
      const reply = "Sorry, please try again later!";
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now() + "_error",
          reply,
          sender: "rnd",
          isEditable: false,
          tool_calls: false,
          isQueryExecuted: true,
          isExecutedOnDB: true,
        },
      ]);
    }

    console.log(data.chat_message, data.reply);
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
    <div
      className={classNames("flex items-start gap-2.5   box-border", {
        "mt-5": !data.isExecutedOnDB,
      })}
    >
      <AiFillAliwangwang
        className="w-8 h-8 rounded-full"
        style={{ visibility: data.isExecutedOnDB ? "hidden" : "visible" }}
      />
      <div className="flex flex-col gap-1 w-full max-w-[320px]">
        <div className="flex items-center space-x-2 rtl:space-x-reverse">
          <span
            className="text-sm font-semibold text-gray-900"
            style={{ display: data.isExecutedOnDB ? "none" : "block" }}
          >
            Rimik Technologies
          </span>
        </div>

        {!data.isQueryExecuted &&
          data.isEditable != "done" &&
          data.isEditable != "cancelled" && (
            <span className="cursor-default w-fit bg-indigo-100 text-indigo-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full">
              Query to be run on the database.
              {/* { <br/> } Click <b>'Continue'</b> to proceed or <b>'Edit'</b> to modify. */}
            </span>
          )}
        {!data.isQueryExecuted && data.isEditable == "done" && (
          <span className="cursor-default w-fit bg-green-100  text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full">
            Query executed on database.
            {/* { <br/> } Click <b>'Continue'</b> to proceed or <b>'Edit'</b> to modify. */}
          </span>
        )}
        {!data.isQueryExecuted && data.isEditable == "cancelled" && (
          <span className="cursor-default w-fit bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full">
            Query execution cancelled.
            {/* { <br/> } Click <b>'Continue'</b> to proceed or <b>'Edit'</b> to modify. */}
          </span>
        )}
        <div className="flex flex-col  w-fit  box-content leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl">
          <p
            className="text-sm font-normal text-gray-900"
            style={{
              display:
                data.isEditable === false ||
                data.isEditable == "done" ||
                data.isEditable == "cancelled"
                  ? "block"
                  : "none",
            }}
          >
            {data.tool_calls && (
              <>

              <CopyBlock
                text={msg}
                language={"sql"}
                className="w-fit"
                // showLineNumbers={2}
                wrapLines
              />
              <p> {data.isOutput}</p>
              </>
            )}
            {!data.tool_calls && <p>{msg}</p>}
          </p>
          <textarea
            className="text-sm font-normal text-gray-900"
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
          {!data.isQueryExecuted && (
            <>
              {data.isEditable !== "done" &&
                data.isEditable !== "cancelled" && (
                  <span
                    onClick={(data) => {
                      handleContinueButton(data);
                    }}
                    className="cursor-pointer bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full "
                  >
                    Continue
                  </span>
                )}

              {data.isEditable === false && data.isEditable !== "done" && (
                <span
                  className="cursor-pointer bg-yellow-100 text-yellow-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full "
                  onClick={handleEditClick}
                >
                  Edit
                </span>
              )}

              {data.isEditable !== "done" &&
                data.isEditable !== "cancelled" && (
                  <span
                    onClick={handleCancelClick}
                    className="cursor-pointer bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full "
                  >
                    Cancel
                  </span>
                )}
            </>
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
        <div className="flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl ">
          <p className="text-sm font-normal text-gray-900 ">{message}</p>
        </div>
      </div>
      <FaRegUserCircle className="w-8 h-8 rounded-full" />
    </div>
  );
};

const ChatArea = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const chatSectionRef = useRef(null);
  useEffect(() => {
    console.log(chatSectionRef);
    if (chatSectionRef.current != null) {
      chatSectionRef.current.scrollTop = chatSectionRef.current.scrollHeight;
    }
  }, [messages]);
  const handleSendMessage = (message) => {
    const newMessage = { id: Date.now(), message, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    getResponse(message, newMessage.id);
  };

  const getResponse = async (message, messageId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/chat`,
        // `/api/chat`,

        { query: message },
        { headers: { "Content-Type": "application/json" } }
      );
      const finalData = response.data[0];
      console.log(response.data[0]);
      if (finalData.query) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now() + "_response",
            reply: finalData.query,
            isAltered: false,
            sender: "rnd",
            isEditable: false,
            question: finalData.question,
            function_name: finalData.function_name,
            answer: finalData.answer,
            tools: finalData.tools,
            uid: finalData.uid,
            tool_calls: finalData.tool_calls,
            tool_call_id: finalData.tool_call_id,
            isQueryExecuted: false,
            isExecutedOnDB: false,
            isOutput: "",
          },
        ]);
      } else {
        const reply = "Sorry, please try again later!";
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now() + "_error",
            sender: "rnd",
            reply: finalData.answer,
            isEditable: false,
            isQueryExecuted: true,
            tool_calls: false,
            isExecutedOnDB: false,
          },
        ]);
      }
    } catch (error) {
      const reply = "Sorry, please try again later!";
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now() + "_error",
          reply,
          sender: "rnd",
          isEditable: false,
          isQueryExecuted: true,
          tool_calls: false,
          isExecutedOnDB: false,
        },
      ]);
    }
  };

  return (
    <>
      <div className="h-screen flex w-screen box-border">
        <div
          className="left w-1/5 mr-20 border-black h-dvh"
          id="left-section"
        ></div>
        <div className="right flex flex-col w-4/5 box-border">
          <div
            id="chat-section"
            className="box-border p-5 py-10 w-full overflow-x-hidden overflow-y-auto"
            ref={chatSectionRef}
            style={{
              alignContent: "center",
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
            className="fixed bottom-0 right-5 self-center overflow-x-hidden overflow-y-auto"
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
