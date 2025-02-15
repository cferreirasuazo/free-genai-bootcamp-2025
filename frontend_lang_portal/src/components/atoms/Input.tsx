import * as React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={`border rounded-md p-2 ${className}`}
      {...props}
    />
  );
});

Input.displayName = "Input";

export { Input }; 