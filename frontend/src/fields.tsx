import { useId, type ReactNode } from "react";
import type { TriState } from "./types";

export function label(code: string): string {
  const words = code.replaceAll("_", " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

interface SelectFieldProps<T extends string> {
  label: string;
  value: T;
  options: readonly T[];
  onChange: (value: T) => void;
  describe?: (value: T) => string;
  hint?: string;
}

export function SelectField<T extends string>(props: SelectFieldProps<T>) {
  const id = useId();
  const describe = props.describe ?? label;
  return (
    <div className="field">
      <label htmlFor={id}>{props.label}</label>
      <select id={id} value={props.value} onChange={(e) => props.onChange(e.target.value as T)}>
        {props.options.map((option) => (
          <option key={option} value={option}>
            {describe(option)}
          </option>
        ))}
      </select>
      {props.hint ? <p className="hint">{props.hint}</p> : null}
    </div>
  );
}

const TRI_STATES: readonly TriState[] = ["yes", "no", "unknown"];

export function TriField(props: {
  label: string;
  value: TriState;
  onChange: (value: TriState) => void;
  hint?: string;
}) {
  return (
    <SelectField
      label={props.label}
      value={props.value}
      options={TRI_STATES}
      onChange={props.onChange}
      {...(props.hint ? { hint: props.hint } : {})}
    />
  );
}

interface InputFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: "date" | "text";
  inputMode?: "decimal";
  pattern?: string;
  placeholder?: string;
  hint?: string;
}

export function InputField(props: InputFieldProps) {
  const id = useId();
  return (
    <div className="field">
      <label htmlFor={id}>{props.label}</label>
      <input
        id={id}
        type={props.type ?? "text"}
        value={props.value}
        onChange={(e) => props.onChange(e.target.value)}
        autoComplete="off"
        {...(props.inputMode ? { inputMode: props.inputMode } : {})}
        {...(props.pattern ? { pattern: props.pattern } : {})}
        {...(props.placeholder ? { placeholder: props.placeholder } : {})}
      />
      {props.hint ? <p className="hint">{props.hint}</p> : null}
    </div>
  );
}

export function CheckField(props: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  const id = useId();
  return (
    <div className="field check">
      <input
        id={id}
        type="checkbox"
        checked={props.checked}
        onChange={(e) => props.onChange(e.target.checked)}
      />
      <label htmlFor={id}>{props.label}</label>
    </div>
  );
}

export function Section(props: { title: string; children: ReactNode }) {
  return (
    <fieldset>
      <legend>{props.title}</legend>
      {props.children}
    </fieldset>
  );
}
