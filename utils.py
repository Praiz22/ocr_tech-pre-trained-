@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-1: #ffffff;
    --bg-2: #fff5eb;
    --bg-3: #ffe7cc;
    --card-bg: rgba(255, 255, 255, 0.24);
    --card-border: rgba(255, 255, 255, 0.36);
    --card-shadow: 0 18px 44px rgba(0, 0, 0, 0.28);
    --text-1: #1f1f1f;
    --text-2: #5a5a5a;
    --brand: #ff7a18;
    --brand-2: #ff4d00;
    --muted: #e9e9e9;
    --success: #0aa574;
    --warning: #d97a00;
    --radius-xl: 22px;
    --radius-lg: 18px;
    --radius-md: 14px;
    --glow-brand: 0 0 16px var(--brand), 0 0 32px var(--brand-2);
}

body {
    background-color: var(--bg-1);
    font-family: 'Inter', sans-serif;
    color: var(--text-1);
    margin: 0;
    padding: 0;
    line-height: 1.6;
    overflow-x: hidden;
}

.main-container {
    padding: 2rem;
    background: radial-gradient(circle at top left, var(--bg-2), transparent),
                radial-gradient(circle at bottom right, var(--bg-3), transparent);
    background-size: 200% 200%;
    animation: gradient-anim 10s ease-in-out infinite alternate;
}

.header {
    text-align: center;
    padding: 2rem 0;
}

.branding {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: var(--brand);
    text-shadow: var(--glow-brand);
}

.subtitle {
    font-size: 1rem;
    color: var(--text-2);
    margin-top: 0.5rem;
}

.app-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-xl);
    backdrop-filter: blur(10px);
    box-shadow: var(--card-shadow);
    padding: 2rem;
    animation: fade-in 0.8s ease-out forwards;
}

h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 1rem;
}

p.status {
    font-size: 1rem;
    color: var(--text-2);
    font-weight: 500;
}

.upload-area {
    border: 2px dashed var(--muted);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    color: var(--text-2);
    font-size: 1.1rem;
    transition: all 0.2s ease-in-out;
}

.upload-area:hover {
    border-color: var(--brand);
}

.image-preview-container {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
    border: 1px dashed var(--muted);
    border-radius: var(--radius-lg);
    padding: 1rem;
    overflow: hidden;
}

.placeholder-image {
    color: var(--text-2);
    text-align: center;
}

.section-preprocess .step,
.section-prediction .result {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--muted);
    font-size: 1rem;
    color: var(--text-1);
    font-weight: 500;
}

.section-preprocess .step:last-child,
.section-prediction .result:last-child {
    border-bottom: none;
}

.section-preprocess .step span,
.section-prediction .result span {
    color: var(--brand-2);
    font-weight: 600;
}

.progress-bar-container {
    width: 100%;
    height: 8px;
    background-color: var(--muted);
    border-radius: 4px;
    margin: 0.5rem 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: var(--brand);
    border-radius: 4px;
    transition: width 0.5s ease-in-out;
}

.metric {
    display: flex;
    align-items: center;
    margin-top: 1rem;
}

.metric span {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--brand-2);
    margin-left: 0.5rem;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.6);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 600px;
    border-radius: var(--radius-xl);
    backdrop-filter: blur(10px);
    box-shadow: var(--card-shadow);
    position: relative;
    text-align: center;
}

.close-btn {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close-btn:hover,
.close-btn:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}

.start-demo {
    background: var(--brand);
    color: white;
    font-weight: 600;
    padding: 1rem 2rem;
    border-radius: var(--radius-lg);
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    margin-top: 2rem;
    display: block;
    margin: 2rem auto;
}

.step-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
}

.step-item {
    text-align: center;
}

.step-number {
    font-size: 2rem;
    font-weight: 700;
    color: var(--brand);
}

.step-text {
    font-size: 0.9rem;
    color: var(--text-2);
}

@keyframes gradient-anim {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 100% 50%;
    }
}

@keyframes fade-in {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 768px) {
    .app-container {
        grid-template-columns: 1fr;
    }
}
