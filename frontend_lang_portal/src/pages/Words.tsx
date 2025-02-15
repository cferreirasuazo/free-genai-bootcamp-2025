import React, { useState } from "react";
import { Typography } from "@/components/atoms/Typography";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";

const Words: React.FC = () => {
  const [words, setWords] = useState([
    // Sample data
    { id: 1, japanese: "始める", romaji: "hajimeru", english: "to start", correct: 10, wrong: 2 },
    // Add more words as needed
  ]);
  const [currentPage, setCurrentPage] = useState(1);
  const wordsPerPage = 50;

  const handlePlaySound = (word: string) => {
    // Implement sound playing logic here
    console.log(`Playing sound for ${word}`);
  };

  const handleSort = (column: string) => {
    // Implement sorting logic here
    console.log(`Sorting by ${column}`);
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const paginatedWords = words.slice(
    (currentPage - 1) * wordsPerPage,
    currentPage * wordsPerPage
  );

  return (
    <div className="p-8">
      <Typography variant="heading" className="text-2xl font-bold mb-6">
        Words
      </Typography>
      <table className="min-w-full bg-white shadow-md rounded-lg">
        <thead>
          <tr className="bg-gray-100">
            <th className="py-2 px-4 text-left" onClick={() => handleSort("japanese")}>
              KANJI <span>▲</span>
            </th>
            <th className="py-2 px-4 text-left" onClick={() => handleSort("romaji")}>
              ROMAJI
            </th>
            <th className="py-2 px-4 text-left" onClick={() => handleSort("english")}>
              ENGLISH
            </th>
            <th className="py-2 px-4 text-left" onClick={() => handleSort("correct")}>
              CORRECT
            </th>
            <th className="py-2 px-4 text-left" onClick={() => handleSort("wrong")}>
              WRONG
            </th>
          </tr>
        </thead>
        <tbody>
          {paginatedWords.map((word) => (
            <tr key={word.id} className="border-b">
              <td className="py-2 px-4 text-blue-600">
                {word.japanese}
                <Button onClick={() => handlePlaySound(word.japanese)} className="ml-2">
                  🔊
                </Button>
              </td>
              <td className="py-2 px-4">{word.romaji}</td>
              <td className="py-2 px-4">{word.english}</td>
              <td className="py-2 px-4 text-green-600">{word.correct}</td>
              <td className="py-2 px-4 text-red-600">{word.wrong}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between mt-4">
        <Button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="bg-gray-200 px-4 py-2 rounded"
        >
          Previous
        </Button>
        <span>
          Page {currentPage} of {Math.ceil(words.length / wordsPerPage)}
        </span>
        <Button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === Math.ceil(words.length / wordsPerPage)}
          className="bg-gray-200 px-4 py-2 rounded"
        >
          Next
        </Button>
      </div>
    </div>
  );
};

export default Words; 