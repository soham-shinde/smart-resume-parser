import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import HRUpload from "./pages/HRUpload";
import SortedResumes from "./pages/SortedResumes";
import "./index.css";

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HRUpload />} />
        <Route path="/results" element={<SortedResumes />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
};

export default App;
