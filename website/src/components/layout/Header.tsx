"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Logo } from "@/components/ui/Logo";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { cn } from "@/library/utils";

const navigation = [
  { name: "About", href: "/about" },
  { name: "Flywheel", href: "/flywheel" },
  { name: "Updates", href: "/updates" },
  { name: "Get Involved", href: "/get-involved" },
  { name: "Distributed", href: "/distributed" },
];

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      setIsScrolled(scrollPosition > 0);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 h-header border-b transition-colors duration-200",
        isScrolled ? "header-solid" : "header-transparent"
      )}
    >
      <Container className="flex h-full items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <Logo size="sm" variant={isScrolled ? "dark" : "light"} />
            <span
              className={cn(
                "font-semibold transition-colors duration-200",
                isScrolled ? "text-white" : "text-white"
              )}
            >
              Neuromosaic
            </span>
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "text-sm font-medium transition-colors duration-200",
                  isScrolled
                    ? "text-neutral-300 hover:text-white"
                    : "text-neutral-200 hover:text-white"
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/docs" className="inline-block">
            <Button
              variant="ghost"
              size="sm"
              className={cn(
                "transition-colors duration-200",
                isScrolled
                  ? "text-neutral-300 hover:text-white hover:bg-white/10"
                  : "text-neutral-200 hover:text-white hover:bg-white/10"
              )}
            >
              Docs
            </Button>
          </Link>
          <Link href="/get-involved" className="inline-block">
            <Button
              size="sm"
              className={cn(
                "transition-colors duration-200",
                isScrolled
                  ? "bg-white text-background-dark hover:bg-neutral-200"
                  : "bg-white/10 text-white hover:bg-white hover:text-background-dark"
              )}
            >
              Join Waitlist
            </Button>
          </Link>
        </div>
      </Container>
    </header>
  );
}
