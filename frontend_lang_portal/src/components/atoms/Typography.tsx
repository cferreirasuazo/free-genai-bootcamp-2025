import * as React from "react";

interface TypographyProps extends React.HTMLAttributes<HTMLParagraphElement> {
  variant?: "body" | "heading" | "subheading";
}

const Typography: React.FC<TypographyProps> = ({ variant = "body", className, ...props }) => {
  const baseStyle = "text-gray-800";
  const variantStyle = {
    body: "text-base",
    heading: "text-2xl font-bold",
    subheading: "text-xl font-semibold",
  };

  return (
    <p className={`${baseStyle} ${variantStyle[variant]} ${className}`} {...props} />
  );
};

export { Typography }; 