import React, {useState} from "react";
import "./App.css";

const App: React.FC = () => {
    const [query, setQuery] = useState("");
    const [prompt, setPrompt] = useState(""); // Added prompt state
    const [sampleTraffic, setSampleTraffic] = useState(""); // Added sample traffic state
    const [response, setResponse] = useState("");

    const handleSubmit = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/api/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({query, prompt, sampleTraffic}), // Including all fields in the request
            });

            if (!res.ok) {
                throw new Error("请求失败");
            }

            const data = await res.json();
            setResponse(data.result || JSON.stringify(data));
        } catch (error) {
            setResponse("请求出错：" + (error as Error).message);
        }
    };

    return (
        <div className="container">
            <h1>啄木鸟deepseek流量分析系统</h1>
            <div className="input-container">
                <div className="prompt-section">
                    <h3>提示词</h3>
                    <textarea
                        className="prompt-textarea"
                        placeholder="输入提示词..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                </div>
                <div className="query-section">
                    <h3>问题</h3>
                    <textarea
                        className="query-textarea"
                        placeholder="请输入你的问题..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>
            </div>
            <div className="sample-traffic-section">
                <h3>示例流量数据</h3>
                <textarea
                    className="sample-traffic-textarea"
                    placeholder="请输入示例流量数据..."
                    value={sampleTraffic}
                    onChange={(e) => setSampleTraffic(e.target.value)}
                />
            </div>
            <button onClick={handleSubmit}>提交</button>
            <div className="response">
                <h3>返回结果：</h3>
                <p>{response}</p>
            </div>
        </div>
    );
};

export default App;