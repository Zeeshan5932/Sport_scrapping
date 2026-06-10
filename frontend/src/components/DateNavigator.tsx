"use client";

import { useState } from "react";

interface DateNavigatorProps {
  onDateChange: (date: string) => void;
}

export default function DateNavigator({ onDateChange }: DateNavigatorProps) {
  const [selectedDate, setSelectedDate] = useState<Date>(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return today;
  });

  const formatDate = (date: Date): string => {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const day = String(date.getDate()).padStart(2, "0");
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    return `${day} ${month}, ${year}`;
  };

  const getDateString = (date: Date): string => {
    return date.toISOString().split("T")[0];
  };

  const handlePrevious = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() - 1);
    setSelectedDate(newDate);
    onDateChange(getDateString(newDate));
  };

  const handleNext = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + 1);
    setSelectedDate(newDate);
    onDateChange(getDateString(newDate));
  };

  return (
    <div className="date-navigator">
      <button className="date-nav-button" onClick={handlePrevious}>
        ◄
      </button>
      <span className="whitespace-nowrap">{formatDate(selectedDate)}</span>
      <button className="date-nav-button" onClick={handleNext}>
        ►
      </button>
    </div>
  );
}
