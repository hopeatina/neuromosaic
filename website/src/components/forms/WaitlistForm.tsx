"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Text } from "@/components/ui/Text";

interface WaitlistFormProps {
  onSuccess?: () => void;
}

export function WaitlistForm({ onSuccess }: WaitlistFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const email = formData.get("email");
    const interests = formData.get("interests");

    try {
      // TODO: Implement actual API call here
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate API call
      onSuccess?.();
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-neutral-700 mb-1"
        >
          Email address
        </label>
        <input
          type="email"
          name="email"
          id="email"
          className="form-input"
          placeholder="you@example.com"
          required
        />
      </div>
      <div>
        <label
          htmlFor="interests"
          className="block text-sm font-medium text-neutral-700 mb-1"
        >
          Areas of interest
        </label>
        <select
          id="interests"
          name="interests"
          className="form-input"
          defaultValue=""
          required
        >
          <option value="" disabled>
            Select an area
          </option>
          <option value="model-development">Model Development</option>
          <option value="infrastructure">Infrastructure</option>
          <option value="documentation">Documentation</option>
          <option value="other">Other</option>
        </select>
      </div>
      {error && (
        <Text textColor="primary" className="text-sm">
          {error}
        </Text>
      )}
      <Button type="submit" size="lg" className="w-full" isLoading={isLoading}>
        Join Waitlist
      </Button>
    </form>
  );
}
