'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardFooter, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"

async function predictRisk(formData: FormData) {
  const response = await fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      Age: Number(formData.get('age')),
      SystolicBP: Number(formData.get('systolicBP')),
      DiastolicBP: Number(formData.get('diastolicBP')),
      HeartRate: Number(formData.get('heartRate')),
      BodyTemp: Number(formData.get('bodyTemp')),
      BS: Number(formData.get('bloodSugar')),
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to predict risk')
  }

  return response.json()
}

export default function MaternalHealthRiskForm() {
  const [prediction, setPrediction] = useState<any | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)
    setPrediction(null)

    try {
      const formData = new FormData(e.currentTarget)
      const result = await predictRisk(formData)
      setPrediction(result)
    } catch (err) {
      setError('An error occurred while predicting risk. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Maternal Health Risk Predictor</CardTitle>
          <CardDescription>Enter your health metrics for a risk prediction.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="age">Age</Label>
              <Input type="number" id="age" name="age" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="systolicBP">Systolic BP</Label>
              <Input type="number" id="systolicBP" name="systolicBP" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="diastolicBP">Diastolic BP</Label>
              <Input type="number" id="diastolicBP" name="diastolicBP" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="heartRate">Heart Rate</Label>
              <Input type="number" id="heartRate" name="heartRate" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bodyTemp">Body Temperature</Label>
              <Input type="number" id="bodyTemp" name="bodyTemp" step="0.1" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bloodSugar">Blood Sugar</Label>
              <Input type="number" id="bloodSugar" name="bloodSugar" step="0.1" required />
            </div>
            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? 'Predicting...' : 'Predict Risk Level'}
            </Button>
          </form>
        </CardContent>
        <CardFooter>
          {prediction && (
            <div className="w-full text-center font-semibold">
              Predicted Risk Level: <span className="text-primary">{prediction.prediction}</span>
            </div>
          )}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}
