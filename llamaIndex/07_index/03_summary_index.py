from llama_index.core import Document, SummaryIndex


# --------------------------------------------------
# 1. Create Documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Operating Systems manage the hardware and software
        resources of a computer. They provide services to
        application programs and manage processes, memory,
        storage, and input/output devices.
        """
    ),

    Document(
        text="""
        Process management is an important responsibility of
        an operating system. A process is a program in execution.
        The operating system creates, schedules, and terminates
        processes and manages communication between them.
        """
    ),

    Document(
        text="""
        Memory management controls the allocation and deallocation
        of memory. The operating system keeps track of which parts
        of memory are being used and which parts are available.
        """
    ),

    Document(
        text="""
        Deadlock is a situation in which processes wait indefinitely
        for resources held by one another. The four necessary
        conditions for deadlock are mutual exclusion, hold and wait,
        no preemption, and circular wait.
        """
    ),
]


# --------------------------------------------------
# 2. Create Summary Index
# --------------------------------------------------

index = SummaryIndex.from_documents(
    documents
)


# --------------------------------------------------
# 3. Display Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("SUMMARY INDEX")
print("=" * 60)

print("\nIndex created successfully!")
print(index)

print("\nIndex Type:")
print(type(index))