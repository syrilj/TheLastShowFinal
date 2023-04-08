import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import WriteNew from "./componets/WriteNew";
import Design from "./componets/Design";
import BlankCard from "./componets/BlankCard";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <Routes>
      <Route element={<Design />}>
        <Route path = "/" element={<BlankCard/>} />
        <Route path = "/newObituary" element={<WriteNew/>} />
      </Route>
    </Routes>
  </BrowserRouter>
);

reportWebVitals();