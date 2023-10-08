#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include "linkedlist.h"
#include "value.h"

// Create a new NULL_TYPE value node.
Value *makeNull(){
    Value *null_node = (Value *)calloc(1, sizeof(Value));
    null_node->type = NULL_TYPE;

    return null_node;
}


// Create a new CONS_TYPE value node.
Value *cons(Value *newCar, Value *newCdr){
    Value *cons_node = (Value *)calloc(1, sizeof(Value));
    cons_node->type = CONS_TYPE;

    cons_node->c.car = newCar;
    cons_node->c.cdr = newCdr;

    return cons_node;

}

// Display the contents of the linked list to the screen in some kind of
// readable format
void display(Value *list){
    Value *cur = list;

    while(cur->type != NULL_TYPE){
        printf("%p \n", list->c.car);
        
        cur = cur->c.cdr;
    }
}

// Return a new list that is the reverse of the one that is passed in. All
// content within the list should be duplicated; there should be no shared
// memory whatsoever between the original list and the new one.
//
// FAQ: What if there are nested lists inside that list?
// ANS: There won't be for this assignment. There will be later, but that will
// be after we've got an easier way of managing memory.
Value *reverse(Value *list){
    Value *new_list = (Value *)calloc(1, sizeof(Value));

    //Value *prev = makeNull();

   Value *cur = list;

    while(cur->type != NULL_TYPE){
        new_list->c.car = cur->c.car;
        cur->c.car = cur->c.cdr;
        new_list->c.cdr = new_list->c.car;
        new_list->c.car = cur->c.car;
    }
    
    return new_list;
}

// Frees up all memory directly or indirectly referred to by list. This includes strings.
//
// FAQ: What if a string being pointed to is a string literal? That throws an
// error when freeing.
//
// ANS: Don't put a string literal into the list in the first place. All strings
// added to this list should be able to be freed by the cleanup function.
//
// FAQ: What if there are nested lists inside that list?
//
// ANS: There won't be for this assignment. There will be later, but that will
// be after we've got an easier way of managing memory.
void cleanup(Value *list){
    if (list->type == STR_TYPE){
        free(list->s);
    }
    else if (list->type == CONS_TYPE){
        free(list->c.car);
        free(list->c.cdr);
    }
}

// Utility to make it less typing to get car value. Use assertions to make sure
// that this is a legitimate operation.
Value *car(Value *list){
    assert(list->type == CONS_TYPE);

    return list->c.car;
}

// Utility to make it less typing to get cdr value. Use assertions to make sure
// that this is a legitimate operation.
Value *cdr(Value *list){
    assert(list->type == CONS_TYPE);

    return list->c.car;
}

// Utility to check if pointing to a NULL_TYPE value. Use assertions to make sure
// that this is a legitimate operation.
bool isNull(Value *value){
    assert(value->type == NULL_TYPE);

    return 1;
}

// Measure length of list. Use assertions to make sure that this is a legitimate
// operation.
int length(Value *value){
    assert((value->type == STR_TYPE) || (value->type == CONS_TYPE));

    if (value->type == STR_TYPE){
        int l = sizeof(value->s) / sizeof(value->s[0]);
    }
    else{
        int l = sizeof(value->c);
    }
}