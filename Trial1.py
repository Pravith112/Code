<script>
const questions = [
  {
    question: "What type of environment do you enjoy working in?",
    options: ["Structured and organized", "Creative and flexible", "Outdoors and hands-on", "Analytical and quiet"],
    careers: ["Manager", "Designer", "Engineer", "Researcher"]
  },
  {
    question: "Which subject did you enjoy the most in school?",
    options: ["Mathematics", "Art", "Biology", "Social Studies"],
    careers: ["Engineer", "Designer", "Doctor", "Lawyer"]
  },
  {
    question: "What motivates you the most?",
    options: ["Problem-solving", "Helping others", "Creating new things", "Leading a team"],
    careers: ["Engineer", "Doctor", "Designer", "Manager"]
  },
  {
    question: "Which skill best describes you?",
    options: ["Analytical thinker", "Empathetic listener", "Innovative creator", "Strategic planner"],
    careers: ["Researcher", "Counselor", "Entrepreneur", "Manager"]
  },
  {
    question: "What’s your ideal work style?",
    options: ["Independent", "Collaborative", "Fieldwork", "Office-based"],
    careers: ["Writer", "Teacher", "Environmentalist", "Administrator"]
  }
];

let currentQuestion = 0;
let scores = {};

function loadQuestion() {
  const questionContainer = document.getElementById("question");
  const optionsContainer = document.getElementById("options");

  const q = questions[currentQuestion];
  questionContainer.textContent = q.question;

  optionsContainer.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.textContent = opt;
    btn.classList.add("option-btn");
    btn.onclick = () => selectOption(q.careers[i]);
    optionsContainer.appendChild(btn);
  });
}

function selectOption(career) {
  if (!scores[career]) scores[career] = 0;
  scores[career]++;
  
  currentQuestion++;
  
  if (currentQuestion < questions.length) {
    loadQuestion();
  } else {
    showResult();
  }
}

function showResult() {
  document.getElementById("quiz").style.display = "none";
  const resultContainer = document.getElementById("result");
  resultContainer.style.display = "block";

  const topCareer = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);

  let description = "";

  switch(topCareer) {
    case "Engineer":
      description = `
        You have a strong analytical and logical mind! ⚙️  
        Engineers thrive in solving complex problems and designing solutions that impact the real world.  
        You likely enjoy math, technology, and understanding how things work.  
        Careers to explore: Civil, Mechanical, Computer, or Software Engineering.  
        Pro tip: Try hands-on projects or robotics clubs to sharpen your skills.
      `;
      break;
    case "Designer":
      description = `
        You’re a creative visionary! 🎨  
        Designers like you love expressing ideas visually and turning imagination into reality.  
        You might excel in areas like graphic design, interior design, fashion, or product design.  
        Creativity and innovation are your superpowers — keep exploring art, digital tools, and trends.  
        Tip: Build a portfolio and experiment with different styles!
      `;
      break;
    case "Doctor":
      description = `
        You have a compassionate and detail-oriented nature. ❤️‍🩹  
        Doctors dedicate their lives to improving others’ health and well-being.  
        Your strength lies in empathy, patience, and scientific curiosity.  
        Whether it’s medicine, research, or healthcare management, your path leads to healing.  
        Tip: Volunteer at health camps or learn about anatomy to get real insights.
      `;
      break;
    case "Manager":
      description = `
        You’re a natural-born leader and strategist! 🧭  
        Managers excel in planning, organizing, and guiding teams toward success.  
        You’re good at communication, problem-solving, and motivating others.  
        Potential careers: Business Management, HR, or Entrepreneurship.  
        Tip: Improve your leadership skills through internships or managing small projects.
      `;
      break;
    case "Researcher":
      description = `
        You’re an explorer of knowledge. 🔬  
        Researchers dive deep into questions and seek logical, evidence-based answers.  
        You enjoy analyzing data, observing trends, and discovering new things.  
        Suitable careers: Scientist, Data Analyst, Academic Researcher.  
        Tip: Read journals and join science fairs to nurture your curiosity.
      `;
      break;
    case "Teacher":
      description = `
        You’re an inspiring communicator and mentor. 📚  
        Teachers shape minds and create a lasting impact on society.  
        You enjoy explaining ideas and watching others grow through your guidance.  
        Tip: Try mentoring or teaching small groups to experience the joy of learning exchange.
      `;
      break;
    case "Lawyer":
      description = `
        You’re persuasive, logical, and justice-driven. ⚖️  
        Lawyers love analyzing complex issues and defending what’s right.  
        You’re likely good at communication, reasoning, and debating.  
        Careers: Advocate, Legal Advisor, Judge, or Policy Analyst.  
        Tip: Stay updated with social issues and sharpen your logical reasoning.
      `;
      break;
    case "Entrepreneur":
      description = `
        You’re bold, creative, and love taking charge. 🚀  
        Entrepreneurs thrive on innovation, risk-taking, and vision.  
        You see opportunities where others see challenges.  
        Tip: Start a small project or online venture to test your ideas in real life.
      `;
      break;
    case "Writer":
      description = `
        You have a gift for words and expression. ✍️  
        Writers turn thoughts into powerful stories and connect with people emotionally.  
        You may excel in journalism, content creation, or scriptwriting.  
        Tip: Start a blog or write short pieces regularly — your words can move minds!
      `;
      break;
    default:
      description = `
        You have a mix of talents and interests! 🌟  
        You might enjoy exploring multiple fields before choosing your ideal path.  
        Tip: Try internships, personality tests, and real-world experiences — your unique combination is your strength.
      `;
  }

  resultContainer.innerHTML = `
    <h2>Your Ideal Career Path: ${topCareer}</h2>
    <p>${description}</p>
    <button onclick="location.reload()" class="restart-btn">Restart Quiz</button>
  `;
}

window.onload = loadQuestion;
</script>
