interface BarChartProps {
  data: Array<{
    day: string
    correct: number
    incorrect: number
  }>
}

export function BarChart({ data }: BarChartProps) {
  const maxValue = Math.max(...data.flatMap(d => [d.correct + d.incorrect]))
  
  return (
    <div className="w-full h-full flex items-end space-x-2">
      {data.map((item, index) => {
        const totalHeight = ((item.correct + item.incorrect) / maxValue) * 100
        const correctHeight = (item.correct / (item.correct + item.incorrect)) * totalHeight
        
        return (
          <div key={index} className="flex-1 flex flex-col items-center">
            <div className="w-full relative" style={{ height: `${totalHeight}%` }}>
              <div
                className="absolute bottom-0 w-full bg-destructive"
                style={{ height: `${totalHeight - correctHeight}%` }}
              />
              <div
                className="absolute bottom-0 w-full bg-primary"
                style={{ height: `${correctHeight}%` }}
              />
            </div>
            <span className="text-sm mt-2">{item.day}</span>
          </div>
        )
      })}
    </div>
  )
} 