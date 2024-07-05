import { useState } from "react";
import "./App.css";
import ChatArea from "./components/ChatArea";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<ChatArea />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
