import { HTMLAttributes, forwardRef } from "react";
import { VariantProps, cva } from "class-variance-authority";
import { cn } from "@/library/utils";

const textVariants = cva("", {
  variants: {
    variant: {
      display: "text-display font-bold leading-tight tracking-tight",
      "display-lg": "text-display-lg font-bold leading-tight tracking-tight",
      h1: "text-h1 font-bold leading-tight",
      h2: "text-h2 font-semibold leading-snug",
      h3: "text-h3 font-medium leading-snug",
      "body-lg": "text-body-lg leading-relaxed",
      body: "text-body leading-relaxed",
      small: "text-small leading-normal",
    },
    textColor: {
      default: "text-neutral-900",
      muted: "text-neutral-700",
      primary: "text-primary",
      white: "text-white",
      gradient: "text-gradient",
    },
    align: {
      left: "text-left",
      center: "text-center",
      right: "text-right",
    },
  },
  defaultVariants: {
    variant: "body",
    textColor: "default",
    align: "left",
  },
});

type TextElement = HTMLParagraphElement;
type TextVariantsProps = VariantProps<typeof textVariants>;

interface TextProps
  extends Omit<HTMLAttributes<TextElement>, keyof TextVariantsProps> {
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "p" | "span" | "div";
  variant?: TextVariantsProps["variant"];
  textColor?: TextVariantsProps["textColor"];
  align?: TextVariantsProps["align"];
}

const Text = forwardRef<TextElement, TextProps>(
  (
    { className, variant, textColor, align, as: Component = "p", ...props },
    ref
  ) => {
    return (
      <Component
        ref={ref}
        className={cn(textVariants({ variant, textColor, align, className }))}
        {...props}
      />
    );
  }
);

Text.displayName = "Text";

export { Text, textVariants };
export type { TextProps };
