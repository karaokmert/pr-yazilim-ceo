/**
 * ClickUp REST istemcisi.
 *
 * Ag katmani globalThis.fetch kullanir (Node 20 yerlesigi) —
 * ek bir HTTP bagimliligi bilerek eklenmedi.
 *
 * KIMLIK: Personal API Token. ClickUp dokumantasyonu (developer.clickup.com)
 * Personal API Token'in Authorization header'ina HAM gonderilecegini soyler:
 *   Authorization: pk_123_ABC
 * "Bearer " oneki YALNIZCA OAuth access token icindir. Onek eklenirse
 * her cagri 401 doner — sessiz degil gurultulu bir ariza, ama teshisi
 * zor oldugu icin burada aciklandi.
 */
export const CLICKUP_API_BASE = 'https://api.clickup.com/api/v2';

/** Bir istegin ne kadar bekleyecegi. Takilan istek kullaniciyi kilitlemez. */
const REQUEST_TIMEOUT_MS = 15_000;

export interface ClickUpStatus {
  status: string;
  color: string;
  /** 'open' | 'custom' | 'closed' — kapali statuyu ayirt etmek icin. */
  type?: string;
  orderindex?: number;
}

export interface ClickUpTask {
  id: string;
  name: string;
  status: ClickUpStatus;
  url: string;
  parent: string | null;
  /** Detay panelinde gosterilir; liste cagrisinda bos olabilir. */
  description?: string | null;
  due_date?: string | null;
  priority?: { priority: string; color: string } | null;
  assignees?: Array<{ id: number; username: string }>;
  list?: { id: string; name: string };
  space?: { id: string };
}

export interface ClickUpUser {
  id: number;
  username: string;
  email: string;
}

export interface ClickUpTeam {
  id: string;
  name: string;
}

/** ClickUp'in dondurdugu hatayi tasiyan tip — cagri yerinde ayirt edilebilsin. */
export class ClickUpApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly endpoint: string
  ) {
    super(message);
    this.name = 'ClickUpApiError';
  }

  /** Token gecersiz/suresi dolmus — cagiran tarafi oturumu temizlemeye yonlendirir. */
  get isAuthError(): boolean {
    return this.status === 401 || this.status === 403;
  }
}

export class ClickUpApi {
  constructor(private readonly tokenProvider: () => Promise<string | undefined>) {}

  /**
   * Her istekte Authorization header'i buradan kurulur.
   * Personal API Token ham gonderilir — "Bearer " onegi YOK (bkz. dosya basi).
   */
  protected async authHeaders(): Promise<Record<string, string>> {
    const token = await this.tokenProvider();
    if (!token) {
      throw new Error('ClickUp oturumu yok — once token girin.');
    }
    return { Authorization: token, 'Content-Type': 'application/json' };
  }

  /**
   * Tum HTTP cagrilarinin tek gecis noktasi.
   *
   * Iki sey burada merkezilestirildi:
   *  - zaman asimi: takilan bir istek AbortSignal.timeout ile kesilir,
   *    yoksa kullanici "yukleniyor"da sonsuza kadar bekler.
   *  - iptal: cagiran bir CancellationToken verirse alttaki istek
   *    GERCEKTEN durdurulur (sonucu atmak yetmez).
   */
  private async request<T>(
    path: string,
    init: { method?: string; body?: unknown } = {},
    signal?: AbortSignal
  ): Promise<T> {
    const headers = await this.authHeaders();
    const timeoutSignal = AbortSignal.timeout(REQUEST_TIMEOUT_MS);
    // Iki sebepten de kesilebilmeli: zaman asimi VEYA cagiranin iptali.
    const combined = signal ? AbortSignal.any([signal, timeoutSignal]) : timeoutSignal;

    let response: Response;
    try {
      // exactOptionalPropertyTypes: body'yi "undefined deger" olarak degil
      // "hic yok" olarak gecmek gerekiyor — RequestInit.body undefined kabul etmez.
      const requestInit: RequestInit = {
        method: init.method ?? 'GET',
        headers,
        signal: combined,
      };
      if (init.body !== undefined) {
        requestInit.body = JSON.stringify(init.body);
      }
      response = await fetch(`${CLICKUP_API_BASE}${path}`, requestInit);
    } catch (err) {
      if (signal?.aborted) {
        throw new Error('Istek iptal edildi.');
      }
      if (err instanceof Error && err.name === 'TimeoutError') {
        throw new ClickUpApiError(
          `ClickUp yanit vermedi (${REQUEST_TIMEOUT_MS / 1000}s zaman asimi).`,
          0,
          path
        );
      }
      throw new ClickUpApiError(
        `ClickUp'a ulasilamadi: ${err instanceof Error ? err.message : String(err)}`,
        0,
        path
      );
    }

    if (!response.ok) {
      // ClickUp hata govdesini JSON olarak doner; okunamazsa durum metnine dus.
      let detail = response.statusText;
      try {
        const body = (await response.json()) as { err?: string; ECODE?: string };
        if (body.err) {
          detail = body.ECODE ? `${body.err} (${body.ECODE})` : body.err;
        }
      } catch {
        // govde JSON degil — statusText yeterli
      }
      throw new ClickUpApiError(detail, response.status, path);
    }

    return (await response.json()) as T;
  }

  /** Token'i dogrular ve sahibini doner. Token girisinde bu cagri kullanilir. */
  async getCurrentUser(signal?: AbortSignal): Promise<ClickUpUser> {
    const data = await this.request<{ user: ClickUpUser }>('/user', {}, signal);
    return data.user;
  }

  /** Token'in eristigi workspace'ler. teamId ayari bostayken secim icin. */
  async listTeams(signal?: AbortSignal): Promise<ClickUpTeam[]> {
    const data = await this.request<{ teams: ClickUpTeam[] }>('/team', {}, signal);
    return data.teams ?? [];
  }

  /**
   * Kullaniciya atanmis task'lar.
   *
   * subtasks=true ile sub task'lar da gelir; agac kurulumunda kok/cocuk
   * ayrimini `parent` alani uzerinden BIZ yapariz. Boylece her sub task
   * icin ayri bir ag cagrisi yapmak gerekmez.
   */
  async listAssignedTasks(
    teamId: string,
    userId: number,
    signal?: AbortSignal
  ): Promise<ClickUpTask[]> {
    const params = new URLSearchParams({
      'assignees[]': String(userId),
      subtasks: 'true',
      include_closed: 'false',
    });
    const data = await this.request<{ tasks: ClickUpTask[] }>(
      `/team/${encodeURIComponent(teamId)}/task?${params.toString()}`,
      {},
      signal
    );
    return data.tasks ?? [];
  }

  /** Tek task detayi. Liste cagrisinda gelmeyen alanlar (description) burada. */
  async getTask(taskId: string, signal?: AbortSignal): Promise<ClickUpTask> {
    return this.request<ClickUpTask>(`/task/${encodeURIComponent(taskId)}`, {}, signal);
  }

  /**
   * Bir listede tanimli statuler.
   *
   * Statu degistirirken sart: ClickUp rastgele string kabul etmez, statu
   * task'in bagli oldugu listede tanimli olmali. Kullaniciya serbest metin
   * yazdirmak yerine bu listeyi secim olarak sunuyoruz.
   */
  async listStatuses(listId: string, signal?: AbortSignal): Promise<ClickUpStatus[]> {
    const data = await this.request<{ statuses: ClickUpStatus[] }>(
      `/list/${encodeURIComponent(listId)}`,
      {},
      signal
    );
    return data.statuses ?? [];
  }

  async updateTaskStatus(taskId: string, status: string, signal?: AbortSignal): Promise<void> {
    await this.request<unknown>(
      `/task/${encodeURIComponent(taskId)}`,
      { method: 'PUT', body: { status } },
      signal
    );
  }
}
