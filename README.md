# Shadow-Code-Compiler

**Shadow Code Compiler (SCC)** is a compiler that translates programs written in the **Shadow Code language** into **Scratch Assembly Language (SASM)**.
You can experiment with SASM in this Scratch project:
👉 [Scratch Project Link](https://scratch.mit.edu/projects/1219146913/)

> ⚠️ Full documentation for Shadow Code Compiler is coming soon.

---

## 🚀 Getting Started

### Compiling Scripts

To compile a program, run:

```bash
(path)/Shadow Code Compiler/ShadowCodeCompiler/scc <filename>
```

You can optionally add two keyword arguments:

* `name` – specify a custom output filename
* `sep` – specify a separator string

**Example:**

```bash
scc calculator.sc sep="/n"
```

---

### 📂 Output

* Compiled code is saved to:

  ```
  (path)/Shadow Code Compiler/out/<filename>.sasm
  ```
* The compiled result is also displayed directly in the terminal.

---

### ⚡ Optional Setup

For convenience, add `scc.bat` to your **PATH** in environment variables.
This allows you to simply run:

```bash
scc <filename>
```

from any directory.

---

## 📌 Notes

* Shadow Code is still evolving, and features may change.
* Documentation will be expanded in future updates.
