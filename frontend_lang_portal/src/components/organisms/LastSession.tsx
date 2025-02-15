import { Progress } from "@/components/atoms/Progress"

export function LastSession() {
  // This would normally come from an API
  const mockData = {
    activity: "Adventure MUD",
    group: "Core Verbs",
    date: "2024-03-15",
    correctAnswers: 15,
    totalQuestions: 20,
  }

  const percentage = (mockData.correctAnswers / mockData.totalQuestions) * 100

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-muted-foreground">Activity</p>
          <p className="font-medium">{mockData.activity}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Group</p>
          <p className="font-medium">{mockData.group}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Date</p>
          <p className="font-medium">{mockData.date}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Score</p>
          <p className="font-medium">{`${mockData.correctAnswers}/${mockData.totalQuestions}`}</p>
        </div>
      </div>
      <Progress value={percentage} className="w-full" />
    </div>
  )
} 