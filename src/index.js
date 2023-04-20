import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import WriteNew from "./componets/WriteNew";
import Design from "./componets/Design";
import Home from "./componets/Home";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <Routes>
      <Route element={<Design />}>
        <Route path = "/" element={<Home/>} />
        <Route path = "/newObituary" element={<WriteNew/>} />
      </Route>
    </Routes>
  </BrowserRouter>
);

reportWebVitals();