import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

rawtext1 = """Hello, World!
Now that you’ve installed Rust, it’s time to write your first Rust program. It’s traditional when learning a new language to write a little program that prints the text Hello, world! to the screen, so we’ll do the same here!

Note: This book assumes basic familiarity with the command line. Rust makes no specific demands about your editing or tooling or where your code lives, so if you prefer to use an integrated development environment (IDE) instead of the command line, feel free to use your favorite IDE. Many IDEs now have some degree of Rust support; check the IDE’s documentation for details. The Rust team has been focusing on enabling great IDE support via rust-analyzer. See Appendix D for more details.

Creating a Project Directory
You’ll start by making a directory to store your Rust code. It doesn’t matter to Rust where your code lives, but for the exercises and projects in this book, we suggest making a projects directory in your home directory and keeping all your projects there.

Open a terminal and enter the following commands to make a projects directory and a directory for the “Hello, world!” project within the projects directory.

For Linux, macOS, and PowerShell on Windows, enter this:

$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
For Windows CMD, enter this:

> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
Writing and Running a Rust Program
Next, make a new source file and call it main.rs. Rust files always end with the .rs extension. If you’re using more than one word in your filename, the convention is to use an underscore to separate them. For example, use hello_world.rs rather than helloworld.rs.

Now open the main.rs file you just created and enter the code in Listing 1-1.

Filename: main.rs

fn main() {
    println!("Hello, world!");
}
Listing 1-1: A program that prints Hello, world!

Save the file and go back to your terminal window in the ~/projects/hello_world directory. On Linux or macOS, enter the following commands to compile and run the file:

$ rustc main.rs
$ ./main
Hello, world!
On Windows, enter the command .\main.exe instead of ./main:

> rustc main.rs
> .\main.exe
Hello, world!
Regardless of your operating system, the string Hello, world! should print to the terminal. If you don’t see this output, refer back to the “Troubleshooting” part of the Installation section for ways to get help.

If Hello, world! did print, congratulations! You’ve officially written a Rust program. That makes you a Rust programmer—welcome!

Anatomy of a Rust Program
Let’s review this “Hello, world!” program in detail. Here’s the first piece of the puzzle:

fn main() {

}
These lines define a function named main. The main function is special: it is always the first code that runs in every executable Rust program. Here, the first line declares a function named main that has no parameters and returns nothing. If there were parameters, they would go inside the parentheses ().

The function body is wrapped in {}. Rust requires curly brackets around all function bodies. It’s good style to place the opening curly bracket on the same line as the function declaration, adding one space in between.

Note: If you want to stick to a standard style across Rust projects, you can use an automatic formatter tool called rustfmt to format your code in a particular style (more on rustfmt in Appendix D). The Rust team has included this tool with the standard Rust distribution, as rustc is, so it should already be installed on your computer!

The body of the main function holds the following code:

    println!("Hello, world!");
This line does all the work in this little program: it prints text to the screen. There are four important details to notice here.

First, Rust style is to indent with four spaces, not a tab.

Second, println! calls a Rust macro. If it had called a function instead, it would be entered as println (without the !). We’ll discuss Rust macros in more detail in Chapter 19. For now, you just need to know that using a ! means that you’re calling a macro instead of a normal function and that macros don’t always follow the same rules as functions.

Third, you see the "Hello, world!" string. We pass this string as an argument to println!, and the string is printed to the screen.

Fourth, we end the line with a semicolon (;), which indicates that this expression is over and the next one is ready to begin. Most lines of Rust code end with a semicolon.

Compiling and Running Are Separate Steps
You’ve just run a newly created program, so let’s examine each step in the process.

Before running a Rust program, you must compile it using the Rust compiler by entering the rustc command and passing it the name of your source file, like this:

$ rustc main.rs
If you have a C or C++ background, you’ll notice that this is similar to gcc or clang. After compiling successfully, Rust outputs a binary executable.

On Linux, macOS, and PowerShell on Windows, you can see the executable by entering the ls command in your shell:

$ ls
main  main.rs
On Linux and macOS, you’ll see two files. With PowerShell on Windows, you’ll see the same three files that you would see using CMD. With CMD on Windows, you would enter the following:

> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
This shows the source code file with the .rs extension, the executable file (main.exe on Windows, but main on all other platforms), and, when using Windows, a file containing debugging information with the .pdb extension. From here, you run the main or main.exe file, like this:

$ ./main # or .\main.exe on Windows
If your main.rs is your “Hello, world!” program, this line prints Hello, world! to your terminal.

If you’re more familiar with a dynamic language, such as Ruby, Python, or JavaScript, you might not be used to compiling and running a program as separate steps. Rust is an ahead-of-time compiled language, meaning you can compile a program and give the executable to someone else, and they can run it even without having Rust installed. If you give someone a .rb, .py, or .js file, they need to have a Ruby, Python, or JavaScript implementation installed (respectively). But in those languages, you only need one command to compile and run your program. Everything is a trade-off in language design.

Just compiling with rustc is fine for simple programs, but as your project grows, you’ll want to manage all the options and make it easy to share your code. Next, we’ll introduce you to the Cargo tool, which will help you write real-world Rust programs.

"""


def summarizer(rawtext):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawtext)
    # print(doc)

    tokens = [token.text for token in doc]

    # print("Tokens: ", tokens)

    word_freq = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())

    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]

    # print(sent_tokens)

    sent_score = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]

    # print(sent_score)

    select_length = int(len(sent_tokens) * 0.3)
    # print(select_length)
    summary = nlargest(select_length, sent_score, key=sent_score.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary[::-1])  # Reverse the order of the summary
    # print("Original Text: " + text)
    # print("Summary: " + summary)

    # print("Length of Original Text: ", len(text.split(' ')))
    # print("Length of Summary: ", len(summary.split(' ')))

    return summary, doc, len(rawtext.split(' ')), len(summary.split(' '))


if __name__ == "__main__":
    text = "If you’re more familiar with a dynamic language, such as Ruby, Python, or JavaScript, you might not be used to compiling and running a program as separate steps. Rust is an ahead-of-time compiled language, meaning you can compile a program and give the executable to someone else, and they can run it even without having Rust installed. If you give someone a .rb, .py, or .js file, they need to have a Ruby, Python, or JavaScript implementation installed (respectively). But in those languages, you only need one command to compile and run your program. Everything is a trade-off in language design."
    print(summarizer(text))