import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <Container className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <Text as="h1" variant="display" className="mb-4">
        404
      </Text>
      <Text as="h2" variant="h2" className="mb-6">
        Page Not Found
      </Text>
      <Text variant="body-lg" textColor="muted" className="mb-8 max-w-xl">
        Sorry, we couldn't find the page you're looking for. Please check the
        URL or navigate back to our homepage.
      </Text>
      <Link href="/" className="inline-block">
        <Button size="lg">Return Home</Button>
      </Link>
    </Container>
  );
}
