import React from "react";
import { useParams, Link } from "react-router-dom";

const WordDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  // Sample data for demonstration
  const word = {
    japanese: "あげる",
    romaji: "ageru",
    english: "to give",
    correct: 1,
    wrong: 0,
    groups: ["Core Verbs"],
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Word Details</h1>
        <Link to="/words" className="text-blue-600 hover:underline">
          Back to Words
        </Link>
      </div>
      <div className="bg-white shadow-md rounded-lg p-6">
        <div className="mb-4">
          <h2 className="text-xl font-semibold">Japanese</h2>
          <p className="text-2xl">{word.japanese}</p>
        </div>
        <div className="mb-4">
          <h2 className="text-xl font-semibold">Romaji</h2>
          <p className="text-lg">{word.romaji}</p>
        </div>
        <div className="mb-4">
          <h2 className="text-xl font-semibold">English</h2>
          <p className="text-lg">{word.english}</p>
        </div>
        <div className="mb-4">
          <h2 className="text-xl font-semibold">Study Statistics</h2>
          <div className="flex space-x-4">
            <div className="bg-gray-100 p-4 rounded-lg">
              <h3 className="text-sm font-medium">Correct Answers</h3>
              <p className="text-green-600 text-xl">{word.correct}</p>
            </div>
            <div className="bg-gray-100 p-4 rounded-lg">
              <h3 className="text-sm font-medium">Wrong Answers</h3>
              <p className="text-red-600 text-xl">{word.wrong}</p>
            </div>
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold">Word Groups</h2>
          <div className="flex space-x-2">
            {word.groups.map((group) => (
              <span
                key={group}
                className="bg-blue-100 text-blue-600 px-3 py-1 rounded-full"
              >
                {group}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WordDetails; 