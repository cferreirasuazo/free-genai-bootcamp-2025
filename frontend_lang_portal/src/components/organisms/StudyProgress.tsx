import { BarChart } from "@/components/molecules/BarChart"

export function StudyProgress() {
  // This would normally come from an API
  const mockData = [
    { day: "Mon", correct: 25, incorrect: 5 },
    { day: "Tue", correct: 30, incorrect: 8 },
    { day: "Wed", correct: 22, incorrect: 3 },
    { day: "Thu", correct: 28, incorrect: 7 },
    { day: "Fri", correct: 35, incorrect: 4 },
  ]

  return (
    <div className="h-[300px]">
      <BarChart data={mockData} />
    </div>
  )
} 