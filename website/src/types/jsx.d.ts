import { SVGProps, DetailedHTMLProps, HTMLAttributes } from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      div: DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement>;
      span: DetailedHTMLProps<HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>;
      p: DetailedHTMLProps<HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement>;
      h1: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h2: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h3: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h4: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h5: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h6: DetailedHTMLProps<HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      button: DetailedHTMLProps<HTMLAttributes<HTMLButtonElement>, HTMLButtonElement>;
      a: DetailedHTMLProps<HTMLAttributes<HTMLAnchorElement>, HTMLAnchorElement>;
      ul: DetailedHTMLProps<HTMLAttributes<HTMLUListElement>, HTMLUListElement>;
      li: DetailedHTMLProps<HTMLAttributes<HTMLLIElement>, HTMLLIElement>;
      form: DetailedHTMLProps<HTMLAttributes<HTMLFormElement>, HTMLFormElement>;
      input: DetailedHTMLProps<HTMLAttributes<HTMLInputElement>, HTMLInputElement>;
      label: DetailedHTMLProps<HTMLAttributes<HTMLLabelElement>, HTMLLabelElement>;
      select: DetailedHTMLProps<HTMLAttributes<HTMLSelectElement>, HTMLSelectElement>;
      option: DetailedHTMLProps<HTMLAttributes<HTMLOptionElement>, HTMLOptionElement>;
      section: DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement>;
      svg: SVGProps<SVGSVGElement>;
      path: SVGProps<SVGPathElement>;
      defs: SVGProps<SVGDefsElement>;
      linearGradient: SVGProps<SVGLinearGradientElement>;
      stop: SVGProps<SVGStopElement>;
    }
  }
} 