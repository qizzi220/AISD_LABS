#include <stdio.h>
#include <string.h>

// Структура задачи
struct Task {
    long long id;
    char description[100];
    int priority;
};

#define QMAX 100

// Структура очереди
struct queue {
    struct Task qu[QMAX];
    int rear;
    int frnt;
    int completed_count;
    long long next_auto_id;// переменная для автоинкремента ID
};

// Инициализация очереди
void init(struct queue *q) {
    q->frnt = 1; // сделано,чтобы при пустой очереди условие frnt > rear работало и мы понимали,что очередь пуста. Как только добавляем элемент, у нас rear = front = 1
    q->rear = 0;
    q->completed_count = 0;
    q->next_auto_id = 1; // автоматическая нумерация начнется с 1
}

// проверка очереди на пустоту 
int isEmpty(struct queue *q) {
    if (q->rear < q->frnt) 
        return 1;
    else 
        return 0;
}

// количество задач в очереди
int size(struct queue *q) {
    if (isEmpty(q)) return 0;
    return q->rear - q->frnt + 1;
}

// очистка очереди
void clear(struct queue *q) {
    q->frnt = 1;
    q->rear = 0;
    printf("Очередь успешно очищена.\n");
}

// проверить, есть ли задача с заданным ID
int containsId(struct queue *q, long long id) {
    for (int h = q->frnt; h <= q->rear; h++) {
        if (q->qu[h].id == id) {
            return 1; // найдено
        }
    }
    return 0; // не найдено
}

// добавление задачи в очередь
void enqueue(struct queue *q, struct Task task, int use_auto_id) {
    if (q->rear >= QMAX - 1) {
        printf("Очередь полна!\n");
        return;
    }

    if (use_auto_id) {
        task.id = q->next_auto_id++; // автоматическая нумерация задач
    } else {
        // запрет добавления задач с одинаковым ID
        if (containsId(q, task.id)) {
            printf("Ошибка: Задача с ID %lld уже существует в очереди!\n", task.id);
            return;
        }
    }

    q->rear++;
    q->qu[q->rear] = task;
    printf("Задача успешно добавлена в очередь! (ID: %lld)\n", task.id);
}

// удаление задачи из начала очереди
struct Task dequeue(struct queue *q) {
    struct Task empty_task = {-1, "Пусто", 0};
    if (isEmpty(q) == 1) {
        printf("Очередь пуста!\n");
        return empty_task;
    }

    struct Task x = q->qu[q->frnt];

    // сдвиг оставшихся элементов влево
    for (int h = q->frnt; h < q->rear; h++) {
        q->qu[h] = q->qu[h + 1];
    }
    q->rear--;
    q->completed_count++; // подсчет выполненных задач

    return x;
}

// просмотр верхнего элемента без удаления
struct Task front(struct queue *q) {
    struct Task empty_task = {-1, "Пусто", 0};
    if (isEmpty(q) == 1) {
        printf("Очередь пуста!\n");
        return empty_task;
    }
    return q->qu[q->frnt];
}

// поиск задачи по ID
struct Task* findById(struct queue *q, long long id) {
    for (int h = q->frnt; h <= q->rear; h++) {
        if (q->qu[h].id == id) {
            return &q->qu[h]; // возвращаем указатель на задачу
        }
    }
    return NULL; // если не найдено
}

// удалить задачу по ID из любого места очереди
int deleteById(struct queue *q, long long id) {
    int found_idx = -1;
    for (int h = q->frnt; h <= q->rear; h++) {
        if (q->qu[h].id == id) {
            found_idx = h;
            break;
        }
    }

    if (found_idx == -1) {
        return 0; // задача не найдена
    }

    // сдвиг всех элементов после удаляемой задачи влево
    for (int h = found_idx; h < q->rear; h++) {
        q->qu[h] = q->qu[h + 1];
    }
    q->rear--;
    return 1; // успешно удалено
}

// вывод всех задач в виде списка
void printQueue(struct queue *q) {
    if (isEmpty(q)) {
        printf("Очередь пуста!\n");
        return;
    }
    printf("\n=== ТЕКУЩИЕ ЗАДАЧИ В ОЧЕРЕДИ ===\n");
    for (int h = q->frnt; h <= q->rear; h++) {
        printf("Позиция: %d | ID: %lld | Приоритет: %d | Описание: %s\n", 
               h - q->frnt + 1, q->qu[h].id, q->qu[h].priority, q->qu[h].description);
    }
    printf("=================================\n");
}

// вывод очереди в виде одной строки
void printQueueAsString(struct queue *q) {
    if (isEmpty(q)) {
        printf("Очередь пуста (строка: [])\n");
        return;
    }
    printf("Строковое представление очереди: ");
    for (int h = q->frnt; h <= q->rear; h++) {
        printf("[ID:%lld | '%s' | Prio:%d]", 
               q->qu[h].id, q->qu[h].description, q->qu[h].priority);
        if (h < q->rear) {
            printf(" -> ");
        }
    }
    printf("\n");
}

// главная функция для демонстрации работы
int main() {
    struct queue q;
    init(&q);
    int choice;
    struct Task temp;
    long long search_id;

    while (1) {
        printf("\n--- МЕНЮ УПРАВЛЕНИЯ ОЧЕРЕДЬЮ ---\n");
        printf("1. Добавить задачу (enqueue)\n");
        printf("2. Выполнить/Удалить первую задачу (dequeue)\n");
        printf("3. Показать первую задачу (front)\n");
        printf("4. Проверить на пустоту (isEmpty)\n");
        printf("5. Показать размер очереди (size)\n");
        printf("6. Очистить очередь (clear)\n");
        printf("7. Вывести все задачи\n");
        printf("8. Вывести очередь в виде строки\n");
        printf("9. Найти задачу по ID\n");
        printf("10. Удалить задачу по ID\n");
        printf("11. Показать количество выполненных задач\n");
        printf("12. Выйти\n");
        printf("Выберите действие: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: {
                int mode;
                printf("Выберите режим ID (1 - Автоматически, 2 - Вручную): ");
                scanf("%d", &mode);
                
                if (mode == 2) {
                    printf("Введите ID задачи: ");
                    scanf("%lld", &temp.id);
                }
                
                printf("Введите приоритет: ");
                scanf("%d", &temp.priority);
                
                printf("Введите описание задачи: ");
                getchar(); // Очистка буфера клавиатуры
                fgets(temp.description, sizeof(temp.description), stdin);
                // Удаление символа переноса строки из fgets
                temp.description[strcspn(temp.description, "\n")] = '\0';

                enqueue(&q, temp, (mode == 1));
                break;
            }
            case 2:
                temp = dequeue(&q);
                if (temp.id != -1) {
                    printf("Выполнена задача: ID %lld | Описание: %s\n", temp.id, temp.description);
                }
                break;
            case 3:
                temp = front(&q);
                if (temp.id != -1) {
                    printf("Первая задача в очереди: ID %lld | Описание: %s\n", temp.id, temp.description);
                }
                break;
            case 4:
                if (isEmpty(&q)) {
                    printf("Очередь пуста.\n");
                } else {
                    printf("В очереди есть задачи.\n");
                }
                break;
            case 5:
                printf("Текущий размер очереди: %d\n", size(&q));
                break;
            case 6:
                clear(&q);
                break;
            case 7:
                printQueue(&q);
                break;
            case 8:
                printQueueAsString(&q);
                break;
            case 9: {
                printf("Введите ID для поиска: ");
                scanf("%lld", &search_id);
                struct Task* found = findById(&q, search_id);
                if (found != NULL) {
                    printf("Найдена задача: ID %lld | Приоритет: %d | Описание: %s\n", 
                           found->id, found->priority, found->description);
                } else {
                    printf("Задача с ID %lld не найдена.\n", search_id);
                }
                break;
            }
            case 10:
                printf("Введите ID задачи для удаления: ");
                scanf("%lld", &search_id);
                if (deleteById(&q, search_id)) {
                    printf("Задача с ID %lld успешно удалена.\n", search_id);
                } else {
                    printf("Ошибка: задача с ID %lld не найдена в очереди.\n", search_id);
                }
                break;
            case 11:
                printf("Количество успешно выполненных задач (через dequeue): %d\n", q.completed_count);
                break;
            case 12:
                return 0;
            default:
                printf("Неверный пункт меню!\n");
        }
    }
    return 0;
}